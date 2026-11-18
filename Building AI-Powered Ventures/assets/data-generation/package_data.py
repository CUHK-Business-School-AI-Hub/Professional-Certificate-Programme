from pathlib import Path
import csv,zipfile,json
ROOT=Path(__file__).resolve().parents[2] / 'data/case2';G=ROOT/'ground-truth'
manifest=json.loads((G/'manifest.json').read_text())
ids=lambda key:', '.join(f'CASE-{n:03d}' for n in manifest[key])
text=f'''# Context to reveal during the exercise

## First Coach loop: confirm the statistical anomaly

After learners inspect their 3-sigma flags, provide the relevant entries in `anomaly_review.csv` and confirm that those particular weeks contain one-off wholesale orders. For this classroom policy, exclude confirmed weeks and renormalise the remaining original weights. Do not give this confirmation before the first run.

## Chatbot context: Member Days

The following SKUs took part in Member Days during both 2-8 November and 9-15 November 2026:

{ids('campaign_sku_ids')}

Sales during those full weeks were about 50% above normal. No Member Day is scheduled for 16-22 November. Estimate normal demand by dividing the relevant non-excluded observations by 1.5. Keep raw sales unchanged, show the proposed rule and its scope, then apply it after review.

## Chatbot context: clearance

Effective 16 November 2026, these SKUs are clearance products and must not receive new replenishment orders:

{ids('clearance_sku_ids')}

Set their recommended new orders to zero even if projected demand is positive. Preserve existing inbound and show the clearance reason. Other SKUs retain their normal rules.

## Optional inbound-delay scenario

The CASE-002 shipment of 50 units is delayed by two days: its expected saleable date moves from 19 November to 21 November. Change only that shipment's date. Preview the resulting quantity and shortage-date changes before applying them.

The hidden actual week includes that delay, but other forecasts must not read future actuals in advance.
'''
(G/'context_messages.md').write_text(text)
allowed={'products.csv','weekly_sales.csv','dataset.json','README.md','Inventory Sample Data.xlsx'}
assert {p.name for p in (ROOT/'student-data').iterdir() if p.is_file()}==allowed
for folder in ['student-data','ground-truth']:
 with zipfile.ZipFile(ROOT/(folder+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((ROOT/folder).rglob('*')):
   if p.is_file():z.write(p,p.relative_to(ROOT))
 with zipfile.ZipFile(ROOT/(folder+'.zip')) as z:assert z.testzip() is None
print('Student and ground-truth packages written separately.')
