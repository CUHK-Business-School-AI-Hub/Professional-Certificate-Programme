# Case 2 reference answer · step-by-step teaching run

Use with Day 1 slides 59–83. Keep [rules.md](rules.md) and [the app](http://127.0.0.1:8765) beside the slides. All products and facts are synthetic. The A–D presets make the finished reference easy to replay; students should still perform the Delegate → Evaluate → Coach work. A–D are cumulative business-context presets, not four development stages: A/B demonstrate the ordinary dashboard; C/D add the facts supplied through the copilot. Loading a preset demonstrates a calculation outcome, not an LLM interpreting a message.

## Loop 1 · Build and evaluate the ordinary dashboard

**Delegate (slides 59–66).** Use the student CSVs, snapshot, weighted-demand rule and daily-stock contract to build the dashboard. Run Stage A: click **A · Baseline**, inspect the reset preview, then **Apply reviewed change**.

**Evaluate (slides 67–68).** The header should show 200 products, 124 needing replenishment, 71 with no order and five needing data. Verify these individual rows:

| SKU | Expected order | Evidence |
| --- | ---: | --- |
| CASE-001 | 68 | Weekly 75.6; daily 10.8; on hand 40; lead 7; safety 3; no inbound |
| CASE-002 | 10 | Weekly 70; on hand 40; 50 inbound on 19 Nov; horizon 10 days |
| CASE-003 / CASE-004 | 0 / 0 | Sufficient inventory / exact target |
| CASE-005 | 13 | Unrounded need 12.285714…; ceil only at the end |
| CASE-006 | 0 | Zero demand; stock cover not applicable |
| CASE-007 | 80 | Empty initial stock; lost demand remains visible before arrival |
| CASE-008 | 10 | Existing inbound outside the planning horizon is excluded |
| CASE-196…200 | Unavailable | Five missing fields are not converted to zero |

Select CASE-001 to see that a 68-unit order still permits a shortage before its 23 Nov arrival. Expand the daily ledger. Order coverage and arrival timing answer different questions.

**Coach (slides 69–70).** Expand Teaching tools and run **Review 3σ candidates**. There should be 12 recent flags, screened against T-13..T-5, using sample standard deviation. Inspect the confirmed wholesale facts, then load and apply Stage B. CASE-013 changes from weekly demand 72.9/order 49 to 28.166667/order 0. T-1 raw sales remain 140; the remaining original weights are divided by 0.6. Recheck CASE-001 at 68. The Stage B count is 120 reorder / 75 no order / 5 needs data.

## Next Step: Add a chatbot as copilot (slide 71)

Introduce Stage 2: work with a chatbot copilot to share new knowledge, explore options and support business judgment. The user confirms changes and makes the decisions. Stage 1 remains the rule-based calculator; Stage 2 adds an LLM at runtime through the chatbot.

## API preparation · before the chatbot (slide 72)

Follow the course API Access Guide, keep the key in the backend `.env`, then start the app. “Key configured” alone does not prove a successful connection. Send the next known-answer question and inspect both the response and tool evidence.

## Loop 2 · Add and evaluate the chatbot

**Delegate (slides 73–74).** The chatbot receives read and preview tools that call the same deterministic engine. It has no apply tool. Ask:

```text
Which products need replenishment? Show the first 10 and the total count.
```

**Evaluate (slide 75).** On Stage B, expect 120 matching products. The tool should be `query_inventory`, and displayed quantities should match the table. Then ask:

```text
Why does CASE-001 need 68 units? Show the weighted weekly demand, daily forecast and exact formula inputs.
```

Expect `inspect_sku`, weighted weekly 75.6, daily 10.8 and order 68. The explanation should mention actual inputs rather than recalculate from guessed values. Expand Evidence to see the returned calculation trail.

**If a real implementation fault appears:** inspect the tool trace, correct the instructions or tool scope, and rerun the same check. This is a repair step, not an additional teaching loop. Continue to business-context coaching below; a correct-looking sentence alone is insufficient evidence.

Ask about a fictional new supplier whose lead time has not been supplied. It should request the missing information. Ask CASE-196's order: it must identify the missing required value and leave the order unavailable.

## Loop 2 continued · Supply business context, review and rerun

**Delegate / Evaluate (slide 77).** On Stage B, inspect CASE-033: weekly forecast 132.8 and order 155. The 3σ check did not flag its Member Day weeks.

**Coach (slide 78).** Copy the complete **Member Days** section from [context_messages.md](../../data/case2/ground-truth/context_messages.md) into the chatbot. It names 32 participant SKUs, both full event weeks, a 50% uplift and no event next week. Expect `preview_business_context`, with 64 SKU/week events. The preview should divide by 1.5, preserve confirmed wholesale exclusions and show CASE-033 changing from 155 to 2. Click Apply, then query it again. Demand is 98.4; raw 150 and 144 are unchanged. The header should show Stage C and 115 reorder SKUs.

**Evaluate / Coach (slides 79–80).** Inspect CASE-063 at order 233. Paste the complete **clearance** section, including the 18 SKUs and effective date. Review the proposed scope, then click Apply. Expect Stage D: 97 reorder, 80 no order, 18 clearance, five missing. CASE-063's new order becomes zero, weekly demand remains 70.2, and shortages remain visible. Existing inbound must remain in the ledger.

The C/D buttons are recovery shortcuts for the instructor. To demonstrate the chatbot's interpretation, use the pasted context and Evidence panel rather than the shortcuts.

## Loop 2 continued · Inbound-delay scenario (slide 81)

Start from a known stage without scenario overrides. Ask:

```text
What if CASE-002’s existing 50-unit inbound shipment is delayed by two days? Preview the order quantity and shortage changes. Keep new-order lead time unchanged.
```

Inspect `preview_inbound_delay`, the date change 19 → 21 November and the ledger:

| Check | Before | Preview after |
| --- | --- | --- |
| New order | 10 | 10 |
| New-order arrival | 23 Nov | 23 Nov |
| First shortage | None | 20 Nov |
| Total lost demand | 0 | 10 |
| Closing stock on 25 Nov | 0 | 10 |

Before clicking Apply, query the dashboard: it must still show 19 Nov and no shortage. Discard to prove that preview has no effect. Repeat, apply, then query CASE-002: the changed date and shortage must now persist. Reload the browser to check persistence. A further two-day delay means two days after the **current** arrival date; reset via a stage button before repeating the original example.

Also test moving the original 19 Nov batch seven days to 26 Nov: the inbound leaves the horizon, order becomes 60 and lost demand is 30. The proposed new order still arrives on 23 Nov.

## Independent exercise and failure checks (slides 82–83)

- CASE-061 combines all three facts: order A/B/C/D = **909 / 334 / 251 / 0**; weekly demand = **496.2 / 209 / 167.5 / 167.5**. Confirm wholesale exclusion first, Member Day division only on remaining weeks, clearance last.
- Check approved change history, restart the server, and confirm the state is reloaded. Return to A before starting a fresh class.
- Simulate API failure with the unit test's injected failing transport. The chatbot reports failure while ordinary calculations remain available. Do not deliberately spend credits with a wrong key.
- Try a stale preview after another change: apply must fail and request a fresh preview.
- Compare forecasts with hidden **customer demand** offline, using `tests/evaluate_forecasts.py`. Do not provide next week's actual outcomes to the chatbot before prediction.
