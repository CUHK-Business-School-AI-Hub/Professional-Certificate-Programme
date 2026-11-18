"""One deterministic calculation engine for the dashboard and all chatbot tools.
Runtime inputs: student CSVs + explicitly approved business events. No answer-key reads.
"""
import csv
import json
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parent
# The distributable ZIP carries its own data; the workspace uses the shared dataset.
CASE = ROOT / 'data' if (ROOT / 'data/student-data').is_dir() else ROOT.parents[1] / 'data/case2'
D = Decimal
WEIGHTS = [D('.4'), D('.3'), D('.2'), D('.1')]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def number(value):
    return round(float(value), 6)


class Engine:
    def __init__(self, data_dir=None):
        data_dir = Path(data_dir or CASE / 'student-data')
        self.settings = json.loads((data_dir / 'dataset.json').read_text())
        self.as_of = date.fromisoformat(self.settings['as_of_date'])
        self.products = {r['sku']: r for r in read_csv(data_dir / 'products.csv')}
        self.history = {sku: [] for sku in self.products}
        for row in read_csv(data_dir / 'weekly_sales.csv'):
            self.history[row['sku']].append(row)
        for rows in self.history.values():
            rows.sort(key=lambda r: r['week_start'], reverse=True)

    def anomalies(self):
        result = []
        for sku, rows in self.history.items():
            older = [float(r['units_sold']) for r in rows[4:13] if r['units_sold'] != '']
            if len(older) != 9:
                continue
            avg, sd = mean(older), stdev(older)
            threshold = avg + 3 * sd
            for r in rows[:4]:
                if r['units_sold'] and float(r['units_sold']) > threshold:
                    result.append({'sku': sku, 'week_start': r['week_start'],
                                   'observed_units': int(r['units_sold']), 'baseline_mean': avg,
                                   'baseline_sample_sd': sd, 'upper_3sigma': threshold,
                                   'review_required': True})
        return result

    def plan(self, sku, state, detail=False):
        if sku not in self.products:
            raise ValueError('Unknown SKU: ' + sku)
        p = dict(self.products[sku])
        p.update(state.get('overrides', {}).get(sku, {}))
        rows = self.history[sku]
        errors = []
        for key in ('on_hand_qty', 'lead_time_days', 'safety_stock_days', 'inbound_qty'):
            if p[key] == '':
                errors.append('Missing ' + key)
        if p['inbound_qty'] and D(str(p['inbound_qty'])) > 0 and not p['inbound_available_date']:
            errors.append('Missing inbound_available_date')
        for r in rows[:4]:
            if r['units_sold'] == '':
                errors.append('Missing units_sold for ' + r['week_start'])
        out = {'sku': sku, 'product_name': p['product_name'], 'category': p['category'],
               'inputs': p, 'status': 'needs_data', 'reason': '; '.join(errors),
               'weekly_forecast_units': None, 'daily_forecast_units': None,
               'planning_days': None, 'eligible_inbound_units': None, 'recommended_order_units': None,
               'first_shortage_date': '', 'unmet_units_over_horizon': None,
               'ending_inventory_units': None, 'excluded_weeks': 0, 'stock_cover_days': None}
        if detail:
            out.update(history=rows, projection=[], calculation=[])
        if errors:
            return out
        events = [e for e in state.get('events', []) if e['sku'] == sku]
        excluded = {e['week_start'] for e in events if e['event_type'] == 'one_off_wholesale'}
        promos = {e['week_start']: D(str(e['multiplier'])) for e in events if e['event_type'] == 'member_day'}
        clearance = any(e['event_type'] == 'clearance' and e['effective_date'] <= self.as_of.isoformat() for e in events)
        total, weight = D(0), D(0)
        calculation = []
        for w, r in zip(WEIGHTS, rows[:4]):
            skip = r['week_start'] in excluded
            adjusted = D(r['units_sold']) / promos.get(r['week_start'], D(1))
            if not skip:
                total += w * adjusted
                weight += w
            calculation.append({'week_start': r['week_start'], 'raw_units': int(r['units_sold']),
                                'original_weight': number(w), 'excluded': skip,
                                'normalised_units': None if skip else number(adjusted),
                                'member_day_multiplier': number(promos.get(r['week_start'], D(1)))})
        if not weight:
            out['reason'] = 'All four recent weeks are excluded; provide an agreed forecast rule.'
            return out
        weekly = total / weight
        daily = weekly / 7
        horizon = int(p['lead_time_days']) + int(p['safety_stock_days'])
        end = self.as_of + timedelta(days=horizon)
        inbound_date = date.fromisoformat(p['inbound_available_date']) if p['inbound_available_date'] else None
        eligible = D(str(p['inbound_qty'])) if inbound_date and self.as_of <= inbound_date < end else D(0)
        target = daily * horizon
        unrounded = max(D(0), target - D(str(p['on_hand_qty'])) - eligible)
        order = 0 if clearance else int(unrounded.to_integral_value(rounding=ROUND_CEILING))
        order_date = self.as_of + timedelta(days=int(p['lead_time_days']))
        stock, unmet, first = D(str(p['on_hand_qty'])), D(0), ''
        projection = []
        for i in range(horizon):
            day = self.as_of + timedelta(days=i)
            inbound = D(str(p['inbound_qty'])) if day == inbound_date else D(0)
            proposed = D(order) if day == order_date else D(0)
            opening = stock
            available = stock + inbound + proposed
            sales = min(available, daily)
            lost = daily - sales
            stock = available - sales
            unmet += lost
            if lost > D('0.000000001') and not first:
                first = day.isoformat()
            projection.append({'date': day.isoformat(), 'opening_stock': number(opening),
                               'existing_inbound': number(inbound), 'proposed_order': number(proposed),
                               'forecast_demand': number(daily), 'sales': number(sales),
                               'unmet_demand': number(lost), 'closing_stock': number(stock)})
        for c in calculation:
            c['effective_weight'] = 0 if c['excluded'] else number(D(str(c['original_weight'])) / weight)
        out.update(weekly_forecast_units=number(weekly), daily_forecast_units=number(daily),
                   planning_days=horizon, planning_end_exclusive=end.isoformat(), eligible_inbound_units=number(eligible),
                   recommended_order_units=order, first_shortage_date=first, unmet_units_over_horizon=number(unmet),
                   ending_inventory_units=number(stock), excluded_weeks=sum(c['excluded'] for c in calculation),
                   status='clearance' if clearance else 'reorder' if order else 'no_order',
                   reason='Clearance: no new orders; existing inbound retained.' if clearance else '',
                   stock_cover_days=number(D(str(p['on_hand_qty'])) / daily) if daily else None,
                   target_demand=number(target), unrounded_order_units=number(unrounded),
                   proposed_order_date=order_date.isoformat())
        if detail:
            shortage_dates = [r['date'] for r in projection if r['unmet_demand'] > 0.000001]
            terms = [f"{c['original_weight']} × {c['raw_units']}" +
                     (f" / {c['member_day_multiplier']}" if c['member_day_multiplier'] != 1 else '')
                     for c in calculation if not c['excluded']]
            out.update(history=rows, projection=projection, calculation=calculation, applied_events=events,
                       shortage_days_count=len(shortage_dates), shortage_dates=shortage_dates,
                       weekly_calculation='(' + ' + '.join(terms) + f') / {weight} = {number(weekly)}',
                       order_calculation=f"ceil(max(0, ({number(weekly)} / 7) × {horizon} − {p['on_hand_qty']} − {number(eligible)}))" +
                           (f' = {order}' if not clearance else f'; clearance overrides the new order to {order}'),
                       planning_period_explanation=f"Planning horizon = lead time {p['lead_time_days']} days + safety-stock {p['safety_stock_days']} days = {horizon} days. The horizon is not the lead time.",
                       timing_note='The aggregate order formula does not add or subtract projected lost demand. '
                           'A new order cannot prevent shortages before its receipt date. '
                           'Shipment delay days and stockout days are different; use shortage_days_count and shortage_dates.')
        return out

    def dashboard(self, state):
        rows = [self.plan(sku, state) for sku in self.products]
        return {'as_of_date': self.as_of.isoformat(), 'version': state['version'],
                'stage': stage_name(state), 'rows': rows, 'counts': dict(Counter(r['status'] for r in rows)),
                'total_order_units': sum(r['recommended_order_units'] or 0 for r in rows),
                'shortage_skus': sum(bool(r['first_shortage_date']) for r in rows),
                'events': state.get('events', []), 'overrides': state.get('overrides', {})}


def stage_name(state):
    # Exact fixture match identifies teaching stages; partial context is explicitly custom.
    events = sorted(state.get('events', []), key=lambda e: (e['sku'], e['event_type'], e.get('week_start') or ''))
    stage = 'A' if not events else 'Custom'
    for candidate in 'BCD':
        known = json.loads((ROOT / 'context' / f'stage_{candidate}.json').read_text())['events']
        if events == sorted(known, key=lambda e: (e['sku'], e['event_type'], e.get('week_start') or '')):
            stage = candidate
    return stage + (' + scenario' if state.get('overrides') else '')
