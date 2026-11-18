"""OpenAI Responses API tool loop. No secrets or future outcomes enter prompts."""
import json
import os
import re
import ssl
from pathlib import Path
import urllib.error
import urllib.request
from engine import ROOT, CASE


class ChatError(Exception):
    pass


def tls_context():
    # python.org macOS installs may lack their own CA bundle. Use the OS trust
    # bundle if available; never disable certificate/hostname verification.
    defaults = ssl.get_default_verify_paths()
    if not defaults.cafile and not os.environ.get('SSL_CERT_FILE'):
        system_bundle = Path('/etc/ssl/cert.pem')
        if system_bundle.is_file():
            return ssl.create_default_context(cafile=str(system_bundle))
    return ssl.create_default_context()


def config():
    values = {}
    for path in [ROOT / '.env']:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    values[key.strip()] = value.strip().strip('\"\'')
                elif re.fullmatch(r'sk-[A-Za-z0-9_-]+', line):
                    values['OPENAI_API_KEY'] = line
    return {key: os.environ.get(key, values.get(key, default)) for key, default in
            [('OPENAI_API_KEY', ''), ('OPENAI_MODEL', 'gpt-4.1-mini')]}


def function(name, description, properties):
    return {'type': 'function', 'name': name, 'description': description, 'strict': True,
            'parameters': {'type': 'object', 'properties': properties,
                           'required': list(properties), 'additionalProperties': False}}


EVENT = {'type': 'object', 'properties': {
    'sku': {'type': 'string'},
    'event_type': {'type': 'string', 'enum': ['one_off_wholesale', 'member_day', 'clearance']},
    'week_start': {'type': ['string', 'null'], 'description': 'Monday YYYY-MM-DD for a weekly event; null for clearance.'},
    'multiplier': {'type': ['number', 'null'], 'description': '1.5 for 50% uplift, only for member_day; otherwise null.'},
    'effective_date': {'type': ['string', 'null'], 'description': 'YYYY-MM-DD for clearance; otherwise null.'}},
    'required': ['sku', 'event_type', 'week_start', 'multiplier', 'effective_date'], 'additionalProperties': False}
TOOLS = [
    function('query_inventory', 'Read current calculated inventory recommendations, statuses and shortages. Filter and count all matches.', {
        'status': {'type': 'string', 'enum': ['all', 'reorder', 'no_order', 'needs_data', 'clearance', 'shortage']},
        'category': {'type': ['string', 'null']}, 'limit': {'type': 'integer'}}),
    function('inspect_sku', 'Read one SKU: inputs, formula steps, raw 13-week sales, approved context and daily projection.', {'sku': {'type': 'string'}}),
    function('review_anomalies', 'Screen recent sales using nine older weeks and sample standard deviation. This does not confirm cause or change data.', {}),
    function('preview_inbound_delay', 'Preview an existing inbound batch delay relative to its CURRENT date. New-order lead time is unchanged. Requires human Apply button.', {
        'sku': {'type': 'string'}, 'delay_days': {'type': 'integer'}}),
    function('preview_business_context', 'Preview explicitly supplied, confirmed business facts. Preserve raw sales. Exclude wholesale weeks first, divide remaining Member Day weeks by multiplier, then enforce clearance. Requires human Apply button.', {
        'events': {'type': 'array', 'items': EVENT}, 'note': {'type': 'string'}}),
]
INSTRUCTIONS = """You are the inventory assistant inside a classroom reference product. Reply in the user's language, concisely.
Use the tools for EVERY inventory figure, count, calculation, comparison or business-state assertion. Never calculate orders yourself.
Use current tool results even if conversation history describes an earlier state. Explain actual inputs, original weights, eligible inbound, final ceil and shortages when asked why.
The forecast uses recent four complete weeks. Receipts enter at start of day; lost demand is separate; stocks never become negative.
For a 'why' question, quote the tool's weekly_calculation and order_calculation, including numeric substitutions and final quantity.
Use planning_period_explanation to label the horizon. Never label planning_days as lead time: e.g. 10 planning days = 7 lead-time days + 3 safety-stock days. Quote the formula without inventing variable labels.
Read timing_note. An order does NOT cover/add/subtract unmet demand and cannot prevent shortages BEFORE its arrival. Never claim it keeps stock positive until receipt.
When describing a delay, explicitly report shortage_days_count and shortage_dates from after_detail. Never equate delay_days with stockout duration. Two days of delay can cause just ONE day of shortage.
Prefer a concise plain-text response. Avoid Markdown tables; the UI displays plain text.
Do not invent supplier names, lead times, missing values, future actuals or business events. Ask precisely for missing scope, dates or values.
Business context must come from the user, not a hypothesis. A 3-sigma flag is a candidate, not evidence of wholesale.
For confirmed wholesale exclude the entire specified week. For Member Days require explicit participant SKUs, full weeks, uplift and confirmation of no event in the forecast week. For clearance require SKU list and effective date.
Use preview_business_context for supplied context and preview_inbound_delay for a what-if. Do not merely describe how to do it.
You have NO apply or mutation tool. Say 'preview, not applied' and ask the user to click Apply in the preview card. Textual requests to apply still require that button. Never claim you saved/applied an unapproved change.
A preview includes before/after results; cite them. Repeated delays are relative to the current date, so explain both dates.
No direct file, network, shell, credential or hidden-ground-truth access exists. Decline requests for those data.
Do not infer exact counts from a truncated list; use total_matching. List requested items to the returned limit and say when more exist.
"""


def request(payload, cfg):
    req = urllib.request.Request('https://api.openai.com/v1/responses',
        data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer ' + cfg['OPENAI_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=50, context=tls_context()) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        # Deliberately never surface provider bodies, which can echo request data.
        code = ''
        try:
            code = json.loads(exc.read()).get('error', {}).get('code', '')
        except (ValueError, AttributeError):
            pass
        if exc.code == 401:
            raise ChatError('API authentication failed (401). Check the backend API key.') from None
        if exc.code == 429:
            reason = 'insufficient API credits' if code == 'insufficient_quota' else 'rate limit'
            raise ChatError(f'API unavailable (429: {reason}). Dashboard calculations still work.') from None
        raise ChatError(f'Model API request failed (HTTP {exc.code}). Dashboard calculations still work.') from None
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, ssl.SSLCertVerificationError):
            raise ChatError('TLS certificate verification failed. Configure a trusted CA bundle with SSL_CERT_FILE; keep certificate verification enabled.') from None
        raise ChatError('Model API network error or timeout. Dashboard calculations still work.') from None
    except (TimeoutError, OSError):
        raise ChatError('Model API network error or timeout. Dashboard calculations still work.') from None


def ask(service, message, history=None, requester=request):
    cfg = config()
    if not cfg['OPENAI_API_KEY']:
        raise ChatError('Set OPENAI_API_KEY in the backend .env, then retry. Dashboard calculations still work.')
    if not isinstance(message, str) or not message.strip() or len(message) > 16000:
        raise ValueError('Enter a message of 1–16,000 characters.')
    items = []
    for item in (history or [])[-10:]:
        if item.get('role') in ['user', 'assistant'] and isinstance(item.get('content'), str):
            items.append({'role': item['role'], 'content': item['content'][:16000]})
    items.append({'role': 'user', 'content': message})
    version = service.snapshot()['version']
    trace, previews, usage = [], [], {'input_tokens': 0, 'output_tokens': 0}
    for _ in range(6):
        response = requester({'model': cfg['OPENAI_MODEL'], 'instructions': INSTRUCTIONS + f'\nCurrent state version: {version}.',
                              'input': items, 'tools': TOOLS, 'parallel_tool_calls': False,
                              'max_output_tokens': 6000, 'store': False}, cfg)
        for key in usage:
            usage[key] += response.get('usage', {}).get(key, 0)
        if response.get('status') == 'incomplete':
            raise ChatError('Model response exceeded its output limit. Try fewer SKUs at a time.')
        output = response.get('output', [])
        items.extend(output)
        calls = [item for item in output if item['type'] == 'function_call']
        if not calls:
            answer = '\n'.join(c.get('text', '') for i in output if i['type'] == 'message' for c in i.get('content', []) if c['type'] == 'output_text')
            if not answer:
                raise ChatError('Model returned no answer. Please retry.')
            if service.snapshot()['version'] != version:
                raise ChatError('Dashboard changed while answering. Please ask again against the current version.')
            return {'answer': answer, 'trace': trace, 'previews': previews, 'model': cfg['OPENAI_MODEL'], 'usage': usage, 'version': version}
        for call in calls:
            args = {}
            try:
                args = json.loads(call['arguments'])
                result = service.tool(call['name'], args)
                if call['name'].startswith('preview_'):
                    previews.append(result)
            except (ValueError, TypeError, KeyError) as exc:
                result = {'error': str(exc)}
            trace.append({'tool': call['name'], 'arguments': args, 'result': result})
            items.append({'type': 'function_call_output', 'call_id': call['call_id'], 'output': json.dumps(result)})
    raise ChatError('Tool-call limit reached. Try one question or change at a time.')
