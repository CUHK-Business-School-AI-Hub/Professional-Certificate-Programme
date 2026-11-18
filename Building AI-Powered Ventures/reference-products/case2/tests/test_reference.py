import copy
import csv
import json
import io
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import Engine, ROOT, CASE
from service import Service, empty_state
from server import create_server
from chat import ask, request, ChatError


def csv_rows(path):
    with path.open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.s = Service()

    def test_01_all_800_ground_truth_plans(self):
        states = {'A': empty_state()}
        for stage in 'BCD':
            states[stage] = {**empty_state(), 'events': json.loads((ROOT / 'context' / f'stage_{stage}.json').read_text())['events']}
        for expected in csv_rows(CASE / 'ground-truth' / 'expected_plans.csv'):
            actual = self.s.engine.plan(expected['sku'], states[expected['stage']])
            with self.subTest(stage=expected['stage'], sku=expected['sku']):
                for key in ['weekly_forecast_units', 'daily_forecast_units', 'planning_days', 'eligible_inbound_units',
                            'recommended_order_units', 'unmet_units_over_horizon', 'ending_inventory_units', 'excluded_weeks']:
                    if expected[key] == '':
                        self.assertIsNone(actual[key], key)
                    else:
                        self.assertAlmostEqual(float(expected[key]), actual[key], places=5, msg=key)
                self.assertEqual(expected['status'], actual['status'])
                self.assertEqual(expected['first_shortage_date'], actual['first_shortage_date'])

    def test_02_hand_answers_and_missing_values(self):
        for sku, order in enumerate([68, 10, 0, 0, 13, 0, 80, 10], 1):
            self.assertEqual(self.s.engine.plan(f'CASE-{sku:03}', self.s.state)['recommended_order_units'], order)
        self.assertIsNone(self.s.engine.plan('CASE-006', self.s.state)['stock_cover_days'])
        missing = [r for r in self.s.engine.dashboard(self.s.state)['rows'] if r['status'] == 'needs_data']
        self.assertEqual(len(missing), 5)
        self.assertTrue(all(r['reason'].startswith('Missing') and r['recommended_order_units'] is None for r in missing))

    def test_03_anomalies_fixed_baseline(self):
        candidates = self.s.engine.anomalies()
        expected = csv_rows(CASE / 'ground-truth' / 'anomaly_review.csv')
        self.assertEqual({(r['sku'], r['week_start']) for r in candidates}, {(r['sku'], r['week_start']) for r in expected})
        self.assertEqual(len(candidates), 12)
        self.assertTrue(all(r['review_required'] for r in candidates))
        self.assertEqual(self.s.state['events'], [])

    def test_04_delay_preview_apply_and_horizon_boundary(self):
        p = self.s.preview_delay('CASE-002', 2)
        a = p['after_detail']
        self.assertEqual(a['recommended_order_units'], 10)
        self.assertEqual(a['first_shortage_date'], '2026-11-20')
        self.assertEqual(a['unmet_units_over_horizon'], 10)
        self.assertEqual(a['ending_inventory_units'], 10)
        self.assertEqual(a['shortage_days_count'], 1)
        self.assertEqual(a['shortage_dates'], ['2026-11-20'])
        self.assertEqual(a['proposed_order_date'], '2026-11-23')
        self.assertEqual(self.s.state['overrides'], {})
        stale = self.s.preview_stage('B')
        self.s.apply(p['id'])
        with self.assertRaises(ValueError): self.s.apply(stale['id'])
        self.assertEqual(self.s.engine.plan('CASE-002', self.s.state)['inputs']['inbound_available_date'], '2026-11-21')
        outside = self.s.preview_delay('CASE-002', 5)['after_detail']
        self.assertEqual(outside['recommended_order_units'], 60)
        self.assertEqual(outside['unmet_units_over_horizon'], 30)
        self.assertEqual(outside['ending_inventory_units'], 30)

    def test_05_inventory_reconciles_and_raw_history_unchanged(self):
        original = copy.deepcopy(self.s.engine.history)
        self.s.apply(self.s.preview_stage('D')['id'])
        for sku in self.s.engine.products:
            for day in self.s.engine.plan(sku, self.s.state, True)['projection']:
                self.assertGreaterEqual(day['closing_stock'], 0)
                self.assertAlmostEqual(day['opening_stock'] + day['existing_inbound'] + day['proposed_order'] - day['sales'], day['closing_stock'], places=5)
                self.assertAlmostEqual(day['sales'] + day['unmet_demand'], day['forecast_demand'], places=5)
        self.assertEqual(original, self.s.engine.history)

    def test_06_scope_priority_and_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            service = Service(Path(tmp) / 'state.json')
            service.apply(service.preview_stage('D')['id'])
            restored = Service(Path(tmp) / 'state.json')
            self.assertEqual(restored.state, service.state)
            self.assertEqual(len(restored.state['audit']), 1)
            for sku in ['CASE-012', 'CASE-032', 'CASE-061', 'CASE-063']:
                plan = restored.engine.plan(sku, restored.state, True)
                self.assertEqual(plan['recommended_order_units'], 0)
                self.assertGreater(plan['weekly_forecast_units'], 0)
            self.assertEqual(restored.engine.plan('CASE-001', restored.state)['recommended_order_units'], 68)

    def test_07_bad_context_does_not_mutate(self):
        for event in [dict(sku='CASE-999', event_type='clearance', week_start=None, multiplier=None, effective_date='2026-11-16'),
                      dict(sku='CASE-033', event_type='member_day', week_start='2026-11-03', multiplier=1.5, effective_date=None),
                      dict(sku='CASE-033', event_type='member_day', week_start='2026-11-02', multiplier=0.5, effective_date=None)]:
            with self.assertRaises(ValueError): self.s.preview_context([event], 'Invalid')
        self.assertEqual(self.s.state, empty_state())

    def test_08_chat_transport_tool_loop_and_api_failure(self):
        outputs = iter([
            {'output': [{'type': 'function_call', 'call_id': 'test1', 'name': 'inspect_sku', 'arguments': '{"sku":"CASE-001"}'}]},
            {'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': 'Order 68 units.'}]}]}
        ])
        with patch('chat.config', return_value={'OPENAI_API_KEY': 'test-only', 'OPENAI_MODEL': 'test'}):
            result = ask(self.s, 'Why CASE-001?', requester=lambda payload, cfg: next(outputs))
            self.assertEqual(result['trace'][0]['result']['recommended_order_units'], 68)
            with self.assertRaises(ChatError):
                ask(self.s, 'Why?', requester=lambda p, c: (_ for _ in ()).throw(ChatError('Simulated timeout')))
        self.assertEqual(self.s.engine.plan('CASE-001', self.s.state)['recommended_order_units'], 68)
        with patch('chat.config', return_value={'OPENAI_API_KEY': '', 'OPENAI_MODEL': 'test'}):
            with self.assertRaises(ChatError): ask(self.s, 'Why?')

    def test_09_http_routes_and_secret_isolation(self):
        server = create_server(0, self.s)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        local_open = urllib.request.build_opener(urllib.request.ProxyHandler({})).open
        try:
            health = json.load(local_open(base + '/api/health'))
            self.assertNotIn('OPENAI_API_KEY', json.dumps(health))
            for path in ['/.env', '/../.env', '/ground-truth/expected_plans.csv', '/service.py']:
                with self.assertRaises(urllib.error.HTTPError) as ctx: local_open(base + path)
                self.assertEqual(ctx.exception.code, 404)
            req = urllib.request.Request(base + '/api/preview-stage', data=b'{"stage":"B"}', headers={'Content-Type': 'application/json'})
            with self.assertRaises(urllib.error.HTTPError) as ctx: local_open(req)
            self.assertEqual(ctx.exception.code, 403)
            req.add_header('X-CSRF-Token', health['csrf'])
            result = json.load(local_open(req))
            self.assertTrue(result['requires_click_to_apply'])
            self.assertEqual(self.s.state['events'], [])
            chat_request = urllib.request.Request(base + '/api/chat', data=b'{"message":"Explain CASE-001"}', headers={'Content-Type': 'application/json', 'X-CSRF-Token': health['csrf']})
            with patch('chat.config', return_value={'OPENAI_API_KEY': '', 'OPENAI_MODEL': 'test'}):
                with self.assertRaises(urllib.error.HTTPError) as ctx:
                    local_open(chat_request)
                self.assertEqual(ctx.exception.code, 502)
                self.assertIn('Dashboard calculations still work', ctx.exception.read().decode())
            self.assertEqual(json.load(local_open(base + '/api/dashboard'))['counts']['reorder'], 124)
        finally:
            server.shutdown(); server.server_close(); thread.join()

    def test_10_provider_failures_are_clear_and_redacted(self):
        cfg = {'OPENAI_API_KEY': 'test-only', 'OPENAI_MODEL': 'test'}
        for status, code, message in [(401, 'invalid_api_key', 'authentication'), (429, 'insufficient_quota', 'insufficient API credits'), (429, 'rate_limit_exceeded', 'rate limit'), (503, '', 'HTTP 503')]:
            body = io.BytesIO(json.dumps({'error': {'code': code, 'message': 'SECRET-SHOULD-NOT-APPEAR'}}).encode())
            error = urllib.error.HTTPError('https://api.openai.com/v1/responses', status, 'test', {}, body)
            with patch('chat.urllib.request.urlopen', side_effect=error):
                with self.assertRaises(ChatError) as ctx:
                    request({}, cfg)
                self.assertIn(message, str(ctx.exception))
                self.assertNotIn('SECRET', str(ctx.exception))
        with patch('chat.urllib.request.urlopen', side_effect=TimeoutError):
            with self.assertRaisesRegex(ChatError, 'timeout'):
                request({}, cfg)


if __name__ == '__main__': unittest.main(verbosity=2)
