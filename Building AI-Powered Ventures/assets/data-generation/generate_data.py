"""Deterministic synthetic inputs and instructor truth. No customer data."""
from pathlib import Path
from datetime import date, timedelta
from fractions import Fraction as F
from collections import Counter
import csv, json, random, math

ROOT = Path(__file__).resolve().parents[2] / 'data/case2'
STUDENT = ROOT / 'student-data'
TRUTH = ROOT / 'ground-truth'
ASOF = date(2026, 11, 16)
SEED = 20261117
RNG = random.Random(SEED)
WEEKS = [ASOF - timedelta(weeks=13-i) for i in range(13)]
WEIGHTS = [F(4,10), F(3,10), F(2,10), F(1,10)]
BULK = set(range(11,21)) | {31,61}
CAMPAIGN = set(range(31,61)) | {11,61}
CLEARANCE = set(range(61,76)) | {12,32,76}
FAMILIES = [('Hair dryer case','Hair care'), ('Headphone case','Audio'),
            ('Controller case','Gaming'), ('Speaker case','Audio'),
            ('Styling tool pouch','Hair care'), ('Cable organiser','Accessories'),
            ('Handheld console case','Gaming'), ('Camera case','Photography')]
COLORS = ['Black','Navy','Grey','Teal','Sand']
SIZES = ['Compact','Standard','Large','Wide','XL']

def dump_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def serialise(x):
    return round(float(x),6) if isinstance(x,F) else x

def alloc(total, weights):
    raw=[total*w/sum(weights) for w in weights]; out=[int(x) for x in raw]
    for i in sorted(range(7), key=lambda i:raw[i]-out[i], reverse=True)[:total-sum(out)]:out[i]+=1
    return out

def plan(product, history, stage, exclusions, events, clearance):
    """Reference policy: exclusions renormalise original time weights."""
    sku=product['sku']; latest=[history[sku][WEEKS[-i-1].isoformat()] for i in range(4)]
    errors=[]
    if any(v is None for v in latest):errors.append('missing_recent_week_sales')
    for k in ('lead_time_days','safety_stock_days'):
        if product[k] is None:errors.append('missing_'+k)
    if product['inbound_qty'] and not product['inbound_available_date']:errors.append('missing_inbound_available_date')
    base={'stage':stage,'sku':sku,'weekly_forecast_units':None,'daily_forecast_units':None,
          'planning_days':None,'eligible_inbound_units':None,'recommended_order_units':None,
          'first_shortage_date':None,'unmet_units_over_horizon':None,'ending_inventory_units':None,
          'excluded_weeks':0,'status':'','reason':''}
    if errors:base.update(status='needs_data',reason=';'.join(errors));return base
    numerator=F(0);denominator=F(0);exclude=0
    for lag,(v,w) in enumerate(zip(latest,WEIGHTS),1):
        week=WEEKS[-lag].isoformat()
        if stage!='A' and (sku,week) in exclusions:exclude+=1;continue
        value=F(v)
        if stage in ('C','D') and (sku,week) in events:value/=F(3,2)
        numerator+=value*w;denominator+=w
    forecast=numerator/denominator
    daily=forecast/7; lead=product['lead_time_days']; horizon=lead+product['safety_stock_days']
    end_exclusive=ASOF+timedelta(days=horizon)
    eta=date.fromisoformat(product['inbound_available_date']) if product['inbound_available_date'] else None
    inbound=product['inbound_qty'] if eta and ASOF<=eta<end_exclusive else 0
    qty=math.ceil(max(F(0),daily*horizon-product['on_hand_qty']-inbound))
    if stage=='D' and sku in clearance:qty=0; reason='clearance_no_replenishment'
    else:reason=''
    stock=F(product['on_hand_qty']);lost=F(0);first=None
    for t in range(horizon):
        today=ASOF+timedelta(days=t)
        if eta==today:stock+=product['inbound_qty']
        if t==lead:stock+=qty
        sold=min(stock,daily);miss=daily-sold;stock-=sold;lost+=miss
        if miss>0 and first is None:first=today.isoformat()
    base.update(weekly_forecast_units=forecast,daily_forecast_units=daily,planning_days=horizon,
                eligible_inbound_units=inbound,recommended_order_units=qty,first_shortage_date=first,
                unmet_units_over_horizon=lost,ending_inventory_units=stock,excluded_weeks=exclude,
                status='clearance' if reason else ('reorder' if qty else 'no_order'),reason=reason)
    return {k:serialise(v) for k,v in base.items()}

def main():
    STUDENT.mkdir(parents=True,exist_ok=True);TRUTH.mkdir(parents=True,exist_ok=True)
    products=[]; sales=[]; causes=[]; issues=[]; profiles=[]; raw_truth={}; full_products={}; exclusions=set(); event_keys=set()
    for i in range(1,201):
        sku=f'CASE-{i:03d}';family,category=FAMILIES[(i-1)%8]
        base=RNG.choice([28,42,56,70,84,98,112,140,168])
        profile=RNG.choices(['stable','rising','falling','intermittent'],[45,25,20,10])[0]
        if i in CAMPAIGN or i in BULK:profile='stable'
        factors=[.72,1.28,.90,1.10,.78,1.22,.94,1.06,1.0]
        early=[max(0,round(base*f)) for f in factors]
        if profile=='intermittent':early=[round(base*f) for f in [0,1.8,0,1.3,.5,0,2,0,1.2]]
        recent_f={'stable':[.98,1.02,.99,1.01],'rising':[.90,.98,1.06,1.14],
                  'falling':[1.14,1.06,.98,.90],'intermittent':[0,1.2,0,.8]}[profile]
        organic=early+[max(0,round(base*f)) for f in recent_f]
        if i in CAMPAIGN:
            organic[-2:]=[2*round(v/2) for v in organic[-2:]]
        # Short, hand-checkable controls alongside the larger batch.
        if i==1:organic=[45,95,50,90,55,85,60,80,70]+[56,63,70,91]
        if i in (2,3,4,10):organic=[50,90,60,80,55,85,65,75,70]+[70]*4
        if i==5:organic=[12,22,14,20,13,21,15,19,17]+[17]*4
        if i==6:organic=[0]*13
        if i==7:organic=[40,72,48,64,44,68,52,60,56]+[56]*4
        if i==8:organic=[10,18,12,16,11,17,13,15,14]+[14]*4
        if i==9:organic=[25,45,30,40,28,42,32,38,35]+[35]*4
        observed=list(organic)
        for j in (11,12):
            if i in CAMPAIGN:
                observed[j]=organic[j]*3//2;event_keys.add((sku,WEEKS[j].isoformat()))
                causes.append({'sku':sku,'event_type':'member_day','week_start':WEEKS[j].isoformat(),
                               'week_end':(WEEKS[j]+timedelta(days=6)).isoformat(),'uplift_multiplier':1.5,
                               'one_off_units':0,'effective_date':'','note':'Full-week event; no repeat event in the validation week.'})
        if i in BULK:
            j=12 if i%2 else 11; extra=base*4
            observed[j]+=extra;exclusions.add((sku,WEEKS[j].isoformat()))
            causes.append({'sku':sku,'event_type':'one_off_wholesale','week_start':WEEKS[j].isoformat(),
                           'week_end':(WEEKS[j]+timedelta(days=6)).isoformat(),'uplift_multiplier':'',
                           'one_off_units':extra,'effective_date':'','note':'Confirmed one-off order; exclude this week after review.'})
        if i in CLEARANCE:
            causes.append({'sku':sku,'event_type':'clearance','week_start':'','week_end':'',
                           'uplift_multiplier':'','one_off_units':0,'effective_date':ASOF.isoformat(),
                           'note':'Do not place new replenishment orders; existing inbound still arrives.'})
        lead=RNG.choice([7,14,21,28]);safety=RNG.choice([3,7,10]);daily=base/7
        stock=max(0,round(daily*(lead+safety)*RNG.choice([.15,.35,.65,1,1.3,1.8])))
        incoming=RNG.random()<.62;in_qty=round(base*RNG.choice([.5,1,1.5,2])) if incoming else 0
        eta=ASOF+timedelta(days=RNG.randint(1,lead+safety+7)) if incoming else None
        if i in CLEARANCE:stock=round(daily*(lead+safety)*.25);in_qty=0;eta=None
        controls={1:(40,7,3,0,None),2:(40,7,3,50,3),3:(140,7,3,0,None),4:(100,7,3,0,None),
                  5:(12,7,3,0,None),6:(25,7,3,0,None),7:(0,7,3,0,None),8:(10,7,3,20,12),
                  9:(80,7,3,20,3),10:(40,7,3,50,9)}
        if i in controls:
            stock,lead,safety,in_qty,offset=controls[i];eta=ASOF+timedelta(days=offset) if offset is not None else None
        if i==199:in_qty=70;eta=ASOF+timedelta(days=4)
        row={'sku':sku,'product_name':f'{family} - {COLORS[((i-1)//8)%5]} - {SIZES[(i-1)//40]}',
             'category':category,'on_hand_qty':stock,'lead_time_days':lead,'safety_stock_days':safety,
             'inbound_qty':in_qty,'inbound_available_date':eta.isoformat() if eta else ''}
        full_products[sku]=dict(row)
        for j,(week,units) in enumerate(zip(WEEKS,observed)):
            raw_truth[(sku,week.isoformat())]=(organic[j],units)
            if (i,j) in ((196,12),(197,10)):
                issues.append({'sku':sku,'file':'weekly_sales.csv','record_key':week.isoformat(),'field':'units_sold','hidden_value':units})
                units=None
            sales.append({'sku':sku,'week_start':week.isoformat(),'week_end':(week+timedelta(days=6)).isoformat(),'units_sold':units})
        for target,field in [(198,'lead_time_days'),(199,'inbound_available_date'),(200,'safety_stock_days')]:
            if i==target:issues.append({'sku':sku,'file':'products.csv','record_key':sku,'field':field,'hidden_value':row[field]});row[field]=None if field!='inbound_available_date' else ''
        products.append(row)
        profiles.append({'sku':sku,'pattern':profile,'latent_base_weekly_units':base})
    history={p['sku']:{} for p in products}
    for row in sales:history[row['sku']][row['week_start']]=row['units_sold']
    clearance={f'CASE-{i:03d}' for i in CLEARANCE}
    plans=[plan(p,history,stage,exclusions,event_keys,clearance) for stage in 'ABCD' for p in products]
    # Future demand is generated from the latent trajectory, not copied from a forecast.
    daily_rows=[];weekly_rows=[];inbounds=[]
    for p,profile in zip(products,profiles):
        sku=p['sku'];i=int(sku[-3:]);actual=full_products[sku];base=profile['latent_base_weekly_units']
        trend={'stable':1,'rising':1.22,'falling':.82,'intermittent':.6}[profile['pattern']]
        demand=max(0,round(base*trend*RNG.uniform(.94,1.06)))
        fixed={1:84,2:70,3:70,4:70,5:17,6:0,7:56,8:14,9:35,10:70}
        demand=fixed.get(i,demand)
        amounts=alloc(demand,[RNG.uniform(.8,1.2) for _ in range(7)])
        if i in (2,3,4,7,8,9,10):amounts=[demand//7]*7
        if i==1:amounts=[12]*7
        if i==5:amounts=[2,3,2,3,2,3,2]
        eta=date.fromisoformat(actual['inbound_available_date']) if actual['inbound_available_date'] else None
        delay=2 if i==2 else (RNG.choices([0,1,2,4],[75,8,13,4])[0] if eta else 0)
        actual_eta=eta+timedelta(days=delay) if eta else None
        if eta:inbounds.append({'sku':sku,'inbound_qty':actual['inbound_qty'],'planned_available_date':eta.isoformat(),
                               'actual_available_date':actual_eta.isoformat(),'delay_days':delay})
        stock=actual['on_hand_qty'];sold_total=lost_total=receipts_total=0
        for day,d in enumerate(amounts):
            dt=ASOF+timedelta(days=day);opening=stock
            receipt=actual['inbound_qty'] if dt==actual_eta else 0
            sold=min(stock+receipt,d);lost=d-sold;stock=stock+receipt-sold
            daily_rows.append({'sku':sku,'date':dt.isoformat(),'opening_inventory':opening,'inbound_received':receipt,
                               'customer_demand':d,'units_sold':sold,'unmet_demand':lost,'closing_inventory':stock})
            sold_total+=sold;lost_total+=lost;receipts_total+=receipt
        weekly_rows.append({'sku':sku,'week_start':ASOF.isoformat(),'week_end':(ASOF+timedelta(days=6)).isoformat(),
                            'customer_demand':demand,'units_sold':sold_total,'unmet_demand':lost_total,
                            'inbound_received':receipts_total,'ending_inventory':stock})
    anomaly=[]
    for p in products:
        sku=p['sku'];values=[history[sku][w.isoformat()] for w in WEEKS[:9]]
        mu=sum(values)/9;sd=math.sqrt(sum((x-mu)**2 for x in values)/8);threshold=mu+3*sd
        for w in WEEKS[-4:]:
            obs=history[sku][w.isoformat()]
            if obs is not None and obs>threshold:
                anomaly.append({'sku':sku,'week_start':w.isoformat(),'observed_units':obs,'baseline_mean':round(mu,6),
                                'baseline_sample_sd':round(sd,6),'upper_3sigma':round(threshold,6),
                                'confirmed_cause':'one_off_wholesale' if (sku,w.isoformat()) in exclusions else 'other'})
    assert {(x['sku'],x['week_start']) for x in anomaly}==exclusions, 'Unexpected 3-sigma flag or missed bulk event'
    scenarios=[]
    p=dict(products[1])
    for label,offset in [('baseline',3),('inbound_delay_2_days',5),('inbound_moves_outside_horizon',10)]:
        p['inbound_available_date']=(ASOF+timedelta(days=offset)).isoformat()
        result=plan(p,history,'D',exclusions,event_keys,clearance)
        scenarios.append({'scenario':label,'inbound_available_date':p['inbound_available_date'],**result})
    dump_csv(STUDENT/'products.csv',products);dump_csv(STUDENT/'weekly_sales.csv',sales)
    config={'synthetic':True,'as_of_date':ASOF.isoformat(),'timezone':'Asia/Hong_Kong',
            'market':'US classroom scenario','warehouse':'Single warehouse','units':'pieces',
            'history_start':WEEKS[0].isoformat(),'history_end':(ASOF-timedelta(days=1)).isoformat(),
            'week_convention':'Monday through Sunday; complete weeks only','weights_newest_to_oldest':[.4,.3,.2,.1],
            'daily_forecast':'weighted_weekly_demand / 7','date_semantics':'Snapshot before demand on as_of_date; arrivals available at start of their date.',
            'future_validation_week_start':ASOF.isoformat(),'future_validation_week_end':(ASOF+timedelta(days=6)).isoformat()}
    (STUDENT/'dataset.json').write_text(json.dumps(config,indent=2)+'\n')
    for name,rows in [('business_events',causes),('data_issues',issues),('expected_plans',plans),('future_daily_actuals',daily_rows),
                      ('future_weekly_actuals',weekly_rows),('inbound_outcomes',inbounds),('anomaly_review',anomaly),('delay_scenarios',scenarios)]:dump_csv(TRUTH/(name+'.csv'),rows)
    breakdown={stage:dict(Counter(x['status'] for x in plans if x['stage']==stage)) for stage in 'ABCD'}
    summary={'seed':SEED,'sku_count':len(products),'historical_week_rows':len(sales),'future_daily_rows':len(daily_rows),
             'bulk_skus':len(BULK),'campaign_skus':len(CAMPAIGN),'clearance_skus':len(CLEARANCE),'three_sigma_flags':len(anomaly),
             'intentional_missing_cells':len(issues),'inbound_batches':len(inbounds),'stage_status_counts':breakdown,
             'category_counts':dict(Counter(p['category'] for p in products)),
             'bulk_sku_ids':sorted(BULK),'campaign_sku_ids':sorted(CAMPAIGN),'clearance_sku_ids':sorted(CLEARANCE)}
    (TRUTH/'manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
    (TRUTH/'generation_profiles.json').write_text(json.dumps(profiles,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
