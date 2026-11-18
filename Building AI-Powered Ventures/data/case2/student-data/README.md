# Replenishment dashboard: student data

All products, sales and shipments are synthetic classroom data. The scenario is a cross-border e-commerce business selling protective cases and pouches, with one warehouse and one outstanding inbound batch at most per SKU.

## Snapshot and files

- Snapshot: **16 November 2026, 00:00, Asia/Hong_Kong**, before that day's demand and receipts.
- History: **17 August to 15 November 2026**, 13 complete Monday-to-Sunday weeks.
- `products.csv`: 200 SKUs and the stock/inbound snapshot.
- `weekly_sales.csv`: 2,600 weekly records. Historical sales are assumed unconstrained by stock availability.
- `dataset.json`: shared date, scope and calculation settings.
- `Inventory Sample Data.xlsx`: a readable copy of the same two input tables. The CSV files are the application inputs; edits to Excel do not automatically update them.

No historical daily sales are supplied. A future daily demand forecast is calculated from weekly data; it is not an observed daily sales history.

## Field dictionary

### products.csv

| Field | Meaning |
|---|---|
| `sku` | Unique identifier. Join records using this field. |
| `product_name` | Fictional case/pouch variant. Names do not imply real device compatibility. |
| `category` | Product category for filtering. |
| `on_hand_qty` | Currently saleable units at the snapshot. Excludes all listed inbound units. |
| `lead_time_days` | Calendar days from a new order at the snapshot to its first saleable date. |
| `safety_stock_days` | Additional demand-coverage days used in the planning rule. |
| `inbound_qty` | Units in the one outstanding batch. Zero means no outstanding inbound. |
| `inbound_available_date` | ISO date when that batch is expected to become saleable, not merely reach port. Blank is valid when inbound quantity is zero; otherwise it is missing data. |

### weekly_sales.csv

| Field | Meaning |
|---|---|
| `sku` | Product identifier. |
| `week_start` | Monday, inclusive. |
| `week_end` | Sunday, inclusive. |
| `units_sold` | Observed units sold that week. Integer zero is valid; an empty field means missing. |

Some required values are intentionally missing. Display a specific data issue for affected SKUs and leave the dependent recommendation unavailable. Do not turn missing values into zeros.

## Initial business rule

`T-1` is 9-15 November, `T-2` is 2-8 November, `T-3` is 26 October-1 November and `T-4` is 19-25 October.

```text
weekly_demand = 0.4*T-1 + 0.3*T-2 + 0.2*T-3 + 0.1*T-4
daily_demand = weekly_demand / 7
planning_days = lead_time_days + safety_stock_days
target_demand = daily_demand * planning_days
recommended_order = ceil(max(0, target_demand - on_hand - eligible_inbound))
```

Eligible inbound arrives on or after the snapshot date and **before** `as_of_date + planning_days`. The planning period includes the snapshot day. For a ten-day period beginning 16 November, include 16-25 November; 26 November is outside it. Keep intermediate precision and round only the final order quantity upwards.

## Daily inventory projection

On each date, add receipts at the start of the day, then satisfy demand:

```text
available = opening_stock + receipts
sales = min(available, daily_demand)
unmet_demand = daily_demand - sales
closing_stock = available - sales
```

Closing stock never becomes negative. In this exercise unmet demand is lost, not carried as a backlog. For a projection with a proposed order, that order arrives at the start of `as_of_date + lead_time_days`. An inbound delay changes the existing batch's date, not the lead time of a new order.

The order formula covers total forecast demand; it does not optimise timing or subtract projected lost sales. Display shortage dates separately. A positive order quantity does not guarantee that stock lasts until delivery.

When all four weeks are zero, demand and the order quantity are zero; stock-cover days are not applicable. Use the full dataset for batch calculations and inspect individual SKUs to explain results.
