# Context to reveal during the exercise

## First Coach loop: confirm the statistical anomaly

After learners inspect their 3-sigma flags, provide the relevant entries in `anomaly_review.csv` and confirm that those particular weeks contain one-off wholesale orders. For this classroom policy, exclude confirmed weeks and renormalise the remaining original weights. Do not give this confirmation before the first run.

## Chatbot context: Member Days

The following SKUs took part in Member Days during both 2-8 November and 9-15 November 2026:

CASE-011, CASE-031, CASE-032, CASE-033, CASE-034, CASE-035, CASE-036, CASE-037, CASE-038, CASE-039, CASE-040, CASE-041, CASE-042, CASE-043, CASE-044, CASE-045, CASE-046, CASE-047, CASE-048, CASE-049, CASE-050, CASE-051, CASE-052, CASE-053, CASE-054, CASE-055, CASE-056, CASE-057, CASE-058, CASE-059, CASE-060, CASE-061

Sales during those full weeks were about 50% above normal. No Member Day is scheduled for 16-22 November. Estimate normal demand by dividing the relevant non-excluded observations by 1.5. Keep raw sales unchanged, show the proposed rule and its scope, then apply it after review.

## Chatbot context: clearance

Effective 16 November 2026, these SKUs are clearance products and must not receive new replenishment orders:

CASE-012, CASE-032, CASE-061, CASE-062, CASE-063, CASE-064, CASE-065, CASE-066, CASE-067, CASE-068, CASE-069, CASE-070, CASE-071, CASE-072, CASE-073, CASE-074, CASE-075, CASE-076

Set their recommended new orders to zero even if projected demand is positive. Preserve existing inbound and show the clearance reason. Other SKUs retain their normal rules.

## Optional inbound-delay scenario

The CASE-002 shipment of 50 units is delayed by two days: its expected saleable date moves from 19 November to 21 November. Change only that shipment's date. Preview the resulting quantity and shortage-date changes before applying them.

The hidden actual week includes that delay, but other forecasts must not read future actuals in advance.
