# Instructor ground truth

This directory contains answers and facts to reveal in stages. Do not distribute it with the initial student data. All observations, including the future validation week, are simulated.

## Three distinct types of truth

1. **Business facts:** `business_events.csv` records one-off wholesale orders, Member Days and clearance decisions. `data_issues.csv` provides the five intentionally withheld field values.
2. **Rule-based expected decisions:** `expected_plans.csv` contains 200 rows for each of four stages (800 rows total). These are reproducible outputs of the stated classroom policy, not a hindsight-optimal order plan.
3. **Next-week outcomes:** `future_weekly_actuals.csv` (200 rows) and `future_daily_actuals.csv` (1,400 rows) cover **16-22 November 2026**. They distinguish customer demand, sales and lost demand; `inbound_outcomes.csv` supplies actual receipt dates for the 111 batches.

`Ground Truth.xlsx` is a readable copy of the principal answer tables. The CSV files contain the complete machine-readable records. `manifest.json` gives generation counts and seed. `generation_profiles.json` records the latent demand pattern; these labels are not student inputs.

## Reveal sequence and calculation policy

| Stage | What the learner knows | Expected rule |
|---|---|---|
| A | Historical sales, stock and planned inbound only | Original weighted four-week demand and aggregate replenishment formula. |
| B | Outlier review confirms one-off wholesale weeks | Exclude confirmed exceptional weeks; renormalise the remaining original time weights. |
| C | Chatbot receives Member Day participants, dates and approximate 50% uplift; no event next week | For non-excluded event weeks, divide recorded sales by 1.5, then apply the same time weights. Preserve raw data. |
| D | Chatbot receives the clearance list, effective at the snapshot | Keep demand estimates visible but set new order quantities to zero for clearance SKUs. Existing inbound remains scheduled. |

`expected_plans.csv` assumes required fields have been checked first. The five incomplete SKUs remain `needs_data` in every stage, with blank dependent results. They do not overlap with clearance SKUs. This makes missing data an explicit issue rather than a plausible zero.

### Stage B: 3-sigma review

Use the **nine older weeks T-13 through T-5** as a fixed baseline. Compute their mean and **sample** standard deviation (denominator n-1), then flag any of the four recent weeks above `mean + 3*sd`. The suspect week never enters its own baseline.

Exactly **12 recent observations on 12 SKUs** exceed the threshold; all correspond to simulated wholesale events. `anomaly_review.csv` records the values and thresholds. The threshold is a screening method; the event record supplies confirmation. Other datasets may contain genuine growth above 3 sigma. A flat zero baseline is not evidence of wholesale by itself.

After confirmation, omit the flagged week's entire observation for this classroom exercise. Do not subtract the one-off quantity and also exclude the week. For example, if T-1 is excluded, the remaining weights become 0.3/0.6, 0.2/0.6 and 0.1/0.6. Do not shift the week positions or replace T-1 with T-5. This simplified exclusion policy sacrifices that week's ordinary sales; later systems may instead separate transaction types.

### Stage C: Member Days

**32 SKUs** participated in full-week events on **2-8 November and 9-15 November**. Recorded sales for those weeks include a 1.5 multiplier. There is no Member Day in the validation week. Divide by 1.5; do not subtract 50%. These uplift-only observations remain below 3 sigma, so a statistical filter cannot supply the missing business context.

For a week containing both wholesale and Member Day effects, retain the Stage B exclusion. Normalise the other event week. Do not overwrite the recorded sales.

### Stage D: clearance

**18 SKUs** are marked for clearance from **16 November 2026**. No new replenishment is allowed even when forecast demand is positive or stockouts are expected. Keep the underlying demand and shortage warning visible and explain why the order is zero.

CASE-011 combines wholesale and Member Day effects; CASE-012 combines wholesale and clearance; CASE-032 combines Member Days and clearance; CASE-061 combines all three. Use these to verify rule priority and scope.

## Future actuals: what they can validate

Future customer demand is independently simulated from the latent sales pattern. It is not copied from a forecast. Member Days and wholesale events do not repeat next week. Normal SKU variation remains, so corrected forecasts will not be exact for every product.

Actual sales are constrained by stock and actual inbound arrivals. Unserved demand is recorded separately and not backordered. Compare demand forecasts against `customer_demand`, not against `units_sold` on stockout weeks.

The actual week follows the existing stock and inbound only. New orders placed on the snapshot cannot arrive within 16-22 November because all true lead times are at least seven days. Therefore these observed outcomes are common to all stages. Use `expected_plans.csv` for rule verification and the daily simulator for longer-horizon order scenarios; do not treat one common realised week as the outcome of every possible ordering policy.

## Hand-checkable examples

| Case | Check |
|---|---|
| CASE-001 | T-1..T-4 = 91, 70, 63, 56. Weighted weekly demand 75.6; daily demand 10.8; inventory 40, lead 7, safety 3, no inbound: order **68**. |
| CASE-002 | Weekly demand 70, inventory 40, inbound 50 on 19 November, lead 7, safety 3: order **10**. |
| CASE-003 | Weekly demand 70, inventory 140, ten-day horizon: order **0**. |
| CASE-004 | Weekly demand 70, inventory 100, ten-day horizon: order **0**, exactly at target. |
| CASE-005 | Weekly demand 17, inventory 12, ten-day horizon: unrounded order 12.285714..., final order **13**. |
| CASE-006 | All weeks zero: demand **0**, order **0**. |
| CASE-007 | Weekly demand 56, inventory zero, ten-day horizon: order **80**; unmet demand before receipt is still visible. |
| CASE-008 | Weekly demand 14, inventory 10; 20 inbound units arrive after the ten-day horizon: order **10**. |

For CASE-002, `delay_scenarios.csv` provides three planning comparisons, all with the proposed order arriving on 23 November:

- Planned inbound on 19 November: order 10; no unmet demand over the ten-day projection.
- Inbound moved two days to 21 November: order still 10; **20 November** has 10 unmet units; closing stock on 25 November is 10.
- Inbound moved to 26 November, outside the horizon: order 60; 30 unmet units before the proposed order arrives; closing stock on 25 November is 30.

The generated actual week includes the two-day delay for CASE-002: demand 70, sales 60, lost demand 10 and ending inventory 30. These are factual simulation outputs, not chatbot instructions given in advance.

## Validation assets

- `validation.json`: executed structural checks, independent known answers, reconciliation and forecast-error comparisons.
- `context_messages.md`: information to reveal after the relevant validation failure, ready for classroom use.
- `data_issues.csv`: answer key for the five missing values; repair only when learners identify the corresponding issue.

The nine-week baseline, full-week event assumption and exclusion policy are teaching choices. They preserve the stated four-week recency weights while keeping the exercise bounded.
