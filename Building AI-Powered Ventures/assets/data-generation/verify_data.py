"""Read the delivered CSVs and verify independent invariants and known answers."""
from pathlib import Path
from datetime import date,timedelta
from collections import Counter,defaultdict
from fractions import Fraction
import csv,json,statistics,math

ROOT=Path(__file__).resolve().parents[2] / 'data/case2'; S=ROOT/'student-data';G=ROOT/'ground-truth'
def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def near(a,b):assert math.isclose(float(a),float(b),abs_tol=1e-5),(a,b)

def main():
    p=rows(S/'products.csv');w=rows(S/'weekly_sales.csv');e=rows(G/'expected_plans.csv')
    daily=rows(G/'future_daily_actuals.csv');weekly=rows(G/'future_weekly_actuals.csv');events=rows(G/'business_events.csv')
    asof=date.fromisoformat(json.loads((S/'dataset.json').read_text())['as_of_date'])
    skus={x['sku'] for x in p};assert len(p)==len(skus)==200
    assert len(w)==2600 and len({(x['sku'],x['week_start']) for x in w})==2600
    assert len(daily)==1400 and len(weekly)==200 and len(e)==800
    bysku=defaultdict(list)
    for r in w:
        assert r['sku'] in skus
        start=date.fromisoformat(r['week_start']);end=date.fromisoformat(r['week_end'])
        assert start.weekday()==0 and end-start==timedelta(days=6) and end<asof
        if r['units_sold']!='':assert int(r['units_sold'])>=0
        bysku[r['sku']].append(r)
    assert all(len(v)==13 for v in bysku.values())
    assert all(int(x['on_hand_qty'])>=0 and int(x['inbound_qty'])>=0 for x in p)
    assert sum(r['units_sold']=='' for r in w)==2
    assert len(rows(G/'data_issues.csv'))==5
    lookup={(r['stage'],r['sku']):r for r in e}
    assert len(lookup)==800
    for stage in 'ABCD':
        for sku in skus:
            r=lookup[stage,sku]
            if r['status']=='needs_data':assert r['recommended_order_units']==''
            else:assert int(r['recommended_order_units'])>=0
    for stage in 'ABCD':
        for n,answer in {1:68,2:10,3:0,4:0,5:13,6:0,7:80,8:10}.items():
            assert int(lookup[stage,f'CASE-{n:03d}']['recommended_order_units'])==answer
    near(lookup['A','CASE-001']['weekly_forecast_units'],75.6)
    # Independent chronological join + integer-weight arithmetic for initial forecasts.
    for sku,rs in bysku.items():
        recent=sorted(rs,key=lambda r:r['week_start'],reverse=True)[:4]
        if any(r['units_sold']=='' for r in recent):continue
        if lookup['A',sku]['status']=='needs_data':continue
        f=Fraction(sum(int(r['units_sold'])*wt for r,wt in zip(recent,[4,3,2,1])),10)
        near(lookup['A',sku]['weekly_forecast_units'],f)
    # Confirm that uplift-only weeks do not accidentally become 3-sigma examples.
    flagged=set()
    for sku,rs in bysku.items():
        rs=sorted(rs,key=lambda r:r['week_start']);base=[int(r['units_sold']) for r in rs[:9]]
        upper=statistics.mean(base)+3*statistics.stdev(base)
        for r in rs[-4:]:
            if r['units_sold'] and int(r['units_sold'])>upper:flagged.add((sku,r['week_start']))
    bulk={(r['sku'],r['week_start']) for r in events if r['event_type']=='one_off_wholesale'}
    assert flagged==bulk and len(flagged)==12
    campaign={r['sku'] for r in events if r['event_type']=='member_day'}
    clearance={r['sku'] for r in events if r['event_type']=='clearance'}
    assert len(campaign)==32 and len(clearance)==18
    for sku in clearance:
        assert int(lookup['C',sku]['recommended_order_units'])>0
        assert lookup['D',sku]['recommended_order_units']=='0' and lookup['D',sku]['status']=='clearance'
    for sku in skus-clearance:
        assert lookup['C',sku]['recommended_order_units']==lookup['D',sku]['recommended_order_units']
    affected=campaign|clearance|{x[0] for x in bulk}
    for sku in skus-affected:
        assert len({lookup[t,sku]['weekly_forecast_units'] for t in 'ABCD'})==1
        assert len({lookup[t,sku]['recommended_order_units'] for t in 'ABCD'})==1
    # Specific overlapping event: CASE-011 loses T-1, not the original time positions.
    recent=sorted(bysku['CASE-011'],key=lambda r:r['week_start'],reverse=True)
    b=Fraction(3*int(recent[1]['units_sold'])+2*int(recent[2]['units_sold'])+int(recent[3]['units_sold']),6)
    c=(Fraction(3*int(recent[1]['units_sold']),1)/Fraction(3,2)+2*int(recent[2]['units_sold'])+int(recent[3]['units_sold']))/6
    near(lookup['B','CASE-011']['weekly_forecast_units'],b);near(lookup['C','CASE-011']['weekly_forecast_units'],c)
    stocks={r['sku']:int(r['on_hand_qty']) for r in p};aggregates=defaultdict(Counter)
    for r in daily:
        sku=r['sku'];dt=date.fromisoformat(r['date']);assert asof<=dt<asof+timedelta(days=7)
        o,inc,demand,sold,lost,close=[int(r[k]) for k in ['opening_inventory','inbound_received','customer_demand','units_sold','unmet_demand','closing_inventory']]
        assert o==stocks[sku] and close==o+inc-sold and demand==sold+lost and min(o,inc,demand,sold,lost,close)>=0
        assert sold==min(o+inc,demand);stocks[sku]=close
        for k in ['customer_demand','units_sold','unmet_demand','inbound_received']:aggregates[sku][k]+=int(r[k])
    for r in weekly:
        for k,v in aggregates[r['sku']].items():assert v==int(r[k])
        assert stocks[r['sku']]==int(r['ending_inventory'])
    row=next(r for r in weekly if r['sku']=='CASE-002')
    assert [int(row[k]) for k in ['customer_demand','units_sold','unmet_demand','ending_inventory']]==[70,60,10,30]
    scen={r['scenario']:r for r in rows(G/'delay_scenarios.csv')}
    for name,qty,lost,closing,first in [('baseline',10,0,0,''),('inbound_delay_2_days',10,10,10,'2026-11-20'),('inbound_moves_outside_horizon',60,30,30,'2026-11-20')]:
        r=scen[name];assert int(r['recommended_order_units'])==qty
        near(r['unmet_units_over_horizon'],lost);near(r['ending_inventory_units'],closing);assert r['first_shortage_date']==first
    demand={r['sku']:int(r['customer_demand']) for r in weekly}
    def mae(stage,subset):
        vals=[abs(float(lookup[stage,k]['weekly_forecast_units'])-demand[k]) for k in subset if lookup[stage,k]['status']!='needs_data']
        return round(sum(vals)/len(vals),4)
    bulk_skus={x[0] for x in bulk}
    assert mae('B',bulk_skus)<mae('A',bulk_skus)
    assert mae('C',campaign)<mae('B',campaign)
    result={'status':'passed','checks':['200 unique SKUs','2600 unique complete-week keys','no future truth in student inputs',
      '12 exact wholesale flags; uplift-only cases below 3 sigma','5 missing-data holds, not zero recommendations',
      '18 clearance overrides; normal controls unchanged','independent time-weight ordering and hand answers',
      'all 1400 daily stock balances and weekly aggregates reconcile','delay and horizon boundary golden cases'],
      'forecast_mae_units_per_week':{'bulk_subset_A':mae('A',bulk_skus),'bulk_subset_B':mae('B',bulk_skus),
      'campaign_subset_B':mae('B',campaign),'campaign_subset_C':mae('C',campaign)},
      'note':'Designed synthetic cases, not evidence of measured production accuracy.'}
    (G/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
