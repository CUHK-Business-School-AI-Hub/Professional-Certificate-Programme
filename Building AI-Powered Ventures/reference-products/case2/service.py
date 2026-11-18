"""Reviewed changes, persistence, and read/preview-only chatbot tools."""
import copy
import json
import os
import threading
import uuid
from datetime import date, timedelta, datetime, timezone
from pathlib import Path
from engine import Engine, ROOT


def empty_state():
    return {'version': 0, 'events': [], 'overrides': {}, 'audit': []}


class Service:
    def __init__(self, state_path=None):
        self.engine = Engine()
        self.path = Path(state_path) if state_path else None
        self.lock = threading.RLock()
        self.state = json.loads(self.path.read_text()) if self.path and self.path.exists() else empty_state()
        self.previews = {}

    def snapshot(self):
        with self.lock:
            return copy.deepcopy(self.state)

    def save(self):
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix('.tmp')
            tmp.write_text(json.dumps(self.state, indent=2))
            os.replace(tmp, self.path)

    def preview(self, proposed, note, base):
        with self.lock:
            if self.state['version'] != base['version']:
                raise ValueError('State changed while calculating. Please preview again.')
            fields = ['weekly_forecast_units', 'recommended_order_units', 'first_shortage_date',
                      'unmet_units_over_horizon', 'status']
            changes = []
            for sku in self.engine.products:
                before, after = self.engine.plan(sku, base), self.engine.plan(sku, proposed)
                if any(before[k] != after[k] for k in fields) or before['inputs'] != after['inputs']:
                    changes.append({'sku': sku, 'before': {k: before[k] for k in fields},
                                    'after': {k: after[k] for k in fields}})
            token = str(uuid.uuid4())
            result = {'id': token, 'base_version': base['version'], 'note': note,
                      'changed_skus': len(changes), 'changes': changes,
                      'events': proposed['events'], 'overrides': proposed['overrides'],
                      'requires_click_to_apply': True}
            self.previews[token] = (copy.deepcopy(proposed), result)
            while len(self.previews) > 50:
                self.previews.pop(next(iter(self.previews)))
            return result

    def apply(self, token):
        with self.lock:
            if token not in self.previews:
                raise ValueError('Preview expired or already applied. Preview again.')
            proposed, preview = self.previews[token]
            if preview['base_version'] != self.state['version']:
                raise ValueError('Preview is stale. Current data changed; preview again.')
            proposed['version'] = self.state['version'] + 1
            proposed['audit'] = self.state['audit'] + [{'version': proposed['version'],
                'at': datetime.now(timezone.utc).isoformat(), 'note': preview['note'],
                'events': proposed['events'], 'overrides': proposed['overrides']}]
            self.state = proposed
            self.save()
            self.previews.clear()
            return {'version': proposed['version'], 'applied': True}

    def preview_stage(self, stage):
        if stage not in ['A', 'B', 'C', 'D']:
            raise ValueError('Choose stage A, B, C or D.')
        base = self.snapshot()
        proposed = copy.deepcopy(base)
        proposed['events'] = [] if stage == 'A' else json.loads((ROOT / 'context' / f'stage_{stage}.json').read_text())['events']
        proposed['overrides'] = {}
        return self.preview(proposed, f'Load instructor stage {stage}; reset scenario overrides', base)

    def preview_delay(self, sku, delay_days):
        if type(delay_days) is not int or not -60 <= delay_days <= 60:
            raise ValueError('delay_days must be an integer from -60 to 60.')
        base = self.snapshot()
        plan = self.engine.plan(sku, base)
        p = plan['inputs']
        if not p['inbound_qty'] or float(p['inbound_qty']) <= 0 or not p['inbound_available_date']:
            raise ValueError('This SKU has no dated outstanding inbound batch. Provide the missing batch details.')
        changed = date.fromisoformat(p['inbound_available_date']) + timedelta(days=delay_days)
        if changed < self.engine.as_of:
            raise ValueError('Arrival cannot precede the snapshot date.')
        proposed = copy.deepcopy(base)
        proposed['overrides'].setdefault(sku, {})['inbound_available_date'] = changed.isoformat()
        result = self.preview(proposed, f'{sku}: existing inbound {p["inbound_available_date"]} → {changed}; new-order lead time unchanged', base)
        result['before_detail'] = self.engine.plan(sku, base, True)
        result['after_detail'] = self.engine.plan(sku, proposed, True)
        return result

    def preview_context(self, events, note):
        if not isinstance(events, list) or not 1 <= len(events) <= 200:
            raise ValueError('Provide between 1 and 200 explicit business events.')
        base = self.snapshot()
        proposed = copy.deepcopy(base)
        keyed = {(e['sku'], e['event_type'], e.get('week_start')): e for e in proposed['events']}
        for e in events:
            if set(e) != {'sku', 'event_type', 'week_start', 'multiplier', 'effective_date'}:
                raise ValueError('Business event fields are incomplete.')
            if e['sku'] not in self.engine.products:
                raise ValueError('Unknown SKU: ' + e['sku'])
            kind = e['event_type']
            if kind not in ['one_off_wholesale', 'member_day', 'clearance']:
                raise ValueError('Unsupported business event type.')
            if kind == 'clearance':
                if not e['effective_date']:
                    raise ValueError('Clearance needs an explicit effective date.')
                date.fromisoformat(e['effective_date'])
                if e['week_start'] is not None or e['multiplier'] is not None:
                    raise ValueError('Clearance has no week_start or multiplier.')
            else:
                recent = {r['week_start'] for r in self.engine.history[e['sku']][:4]}
                if e['week_start'] not in recent:
                    raise ValueError('Specify a complete recent week by its Monday date.')
                if e['effective_date'] is not None:
                    raise ValueError('Weekly events have no effective_date.')
                if kind == 'member_day':
                    if type(e['multiplier']) not in (int, float) or not 1 < e['multiplier'] <= 10:
                        raise ValueError('Member Day requires an explicit uplift multiplier > 1 and <= 10.')
                elif e['multiplier'] is not None:
                    raise ValueError('Wholesale exclusions do not have a multiplier.')
            keyed[(e['sku'], kind, e.get('week_start'))] = dict(e)
        proposed['events'] = list(keyed.values())
        return self.preview(proposed, note[:1500], base)

    def tool(self, name, args):
        state = self.snapshot()
        if name == 'inspect_sku':
            return self.engine.plan(args['sku'], state, True)
        if name == 'query_inventory':
            status, category, limit = args['status'], args['category'], args['limit']
            if status not in ['all', 'reorder', 'no_order', 'needs_data', 'clearance', 'shortage']:
                raise ValueError('Unknown status filter.')
            if type(limit) is not int or not 1 <= limit <= 200:
                raise ValueError('limit must be between 1 and 200.')
            data = self.engine.dashboard(state)
            rows = [r for r in data['rows'] if (status == 'all' or r['status'] == status or status == 'shortage' and r['first_shortage_date']) and (not category or r['category'].lower() == category.lower())]
            keys = ['sku', 'category', 'recommended_order_units', 'weekly_forecast_units', 'first_shortage_date', 'unmet_units_over_horizon', 'status', 'reason']
            return {'version': state['version'], 'stage': data['stage'], 'total_matching': len(rows),
                    'returned': min(limit, len(rows)), 'counts_all_products': data['counts'],
                    'rows': [{k: r[k] for k in keys} for r in rows[:limit]]}
        if name == 'review_anomalies':
            return {'policy': 'T-13..T-5 mean + 3 sample SD; candidates require business confirmation before exclusion.',
                    'candidates': self.engine.anomalies()}
        if name == 'preview_inbound_delay':
            return self.preview_delay(**args)
        if name == 'preview_business_context':
            return self.preview_context(**args)
        raise ValueError('Unknown tool.')
