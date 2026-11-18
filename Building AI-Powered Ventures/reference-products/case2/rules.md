# Case 2 calculation and review contract

Snapshot: 2026-11-16, before daily receipts and demand. Synthetic data only.

1. Read `../student-data/products.csv` and `weekly_sales.csv`. A blank is missing, never zero. The five incomplete SKUs retain `needs_data` in all reference stages.
2. Use T-1..T-4 with original weights 0.4, 0.3, 0.2, 0.1. Keep full Decimal precision until final upward rounding of orders.
3. Stage B: screen recent observations against the fixed nine older weeks' mean + three **sample** standard deviations. A flag requires business confirmation. Exclude the entire confirmed wholesale week and renormalise remaining original weights.
4. Stage C: for explicitly identified full Member Day weeks, divide non-excluded sales by 1.5. Exclusion takes priority. Raw CSV observations remain unchanged. There is no Member Day in the validation week.
5. Daily demand = corrected weighted weekly demand / 7. Planning days = lead time + safety-stock days.
6. Eligible inbound arrives on/after the snapshot and strictly before snapshot + planning days. Order = ceil(max(0, daily demand × planning days − on hand − eligible inbound)).
7. Stage D: effective clearance prohibits new orders but retains the forecast and existing inbound. Missing required data is checked before this rule.
8. Project each day: receipts at start, sales capped at available stock, closing stock ≥ 0; unmet demand is lost, not backlog. Proposed orders arrive at snapshot + lead time. Aggregate order quantity does not compensate for receipt timing: display shortages separately.
9. An inbound delay moves only the current outstanding batch's date. It never changes a new order's lead time.
10. All context/date changes are previews. A human reviews exact events, scope and result differences, then clicks Apply. Previews are versioned; stale or already applied previews fail. Approved context, overrides and an audit history persist in ignored `local-state/state.json`.
11. The chatbot queries the same engine as the dashboard. It cannot apply changes, read files, fetch hidden actuals, repair unknown values or invent supplier lead times. Model responses and tool evidence are shown separately.
12. Hidden expected plans and future actuals are offline evaluation inputs only. Forecast accuracy compares with **customer demand**, not stock-constrained sales. A common actual week does not establish the outcome of alternative longer-horizon order policies.

Business facts live in approved state and instructor `context/stage_*.json` presets. This file records how the program treats them. Changing this text alone does not change executable rules; update `engine.py` and rerun the tests.
