"""Offline evaluation against hidden synthetic customer demand (never an app input)."""
import csv
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import CASE, ROOT
from service import Service

service = Service()
with (CASE / 'ground-truth/future_weekly_actuals.csv').open(encoding='utf-8-sig') as f:
    actuals = {r['sku']: r for r in csv.DictReader(f)}
result = {'snapshot': '2026-11-16', 'validation_week': '2026-11-16 to 2026-11-22',
          'metric': 'sum(abs(forecast - customer_demand)) / sum(customer_demand)', 'stages': {}}
for stage in 'ABCD':
    service.apply(service.preview_stage(stage)['id'])
    board = service.engine.dashboard(service.state)
    complete = [r for r in board['rows'] if r['weekly_forecast_units'] is not None]
    errors = sum(abs(r['weekly_forecast_units'] - float(actuals[r['sku']]['customer_demand'])) for r in complete)
    demand = sum(float(actuals[r['sku']]['customer_demand']) for r in complete)
    result['stages'][stage] = {'sku_count': len(complete), 'WAPE_percent': round(100 * errors / demand, 4),
                               'counts': board['counts'], 'total_order_units': board['total_order_units']}
assert result['stages']['B']['WAPE_percent'] < result['stages']['A']['WAPE_percent']
assert result['stages']['C']['WAPE_percent'] < result['stages']['B']['WAPE_percent']
assert result['stages']['D']['WAPE_percent'] == result['stages']['C']['WAPE_percent']
print(json.dumps(result, indent=2))
