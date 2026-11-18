# Instructor notes · Slides 45–83

This folder covers only the two cases from slide 45 onwards (currently slides 45–83). Earlier methodology is referenced only where needed for the exercises; it is not repeated as lecture notes.

Start with [Instructor Outline](Instructor%20Outline.md). Use [Slide Notes](Slide%20Notes.md) for page-level prompts, reference values and source limits. The notes contain instructor answers.

| Teaching point | Give learners | Keep with the instructor |
|---|---|---|
| Case 1 introduction, slides 45–49 | Business scenario and expected report structure | The finished reference skill |
| Case 1 first attempt, slides 50–53 | Their own brand, market and time window; acceptance criteria | The finished reference skill |
| Case 1 coaching, slides 54–58 | Verified domain rules and a review of changes | Prior findings should not substitute for their own search |
| Case 2 first build, slides 59–67 | `data/case2/student-data.zip` only | Ground truth, presets and reference app |
| Case 2 anomaly evaluation, slides 68–70 | Relevant comparison and reviewed wholesale facts | Other business events until the later exercise |
| Copilot stage, slides 71–81 | API setup, then relevant Member Day, clearance and shipment context | Unrelated hidden answers |
| Independent exercise and reference review | Relevant CASE-061 context; reference products after practice | Private `.env` and local state |

## Case 1

The [reference workflow](../reference-products/case1/README.md) supplies the finished skill and a dated source-review example. Run the initial exercise without it; agree on what counts as good, inspect a real gap, coach the procedure, inspect the rule change and rerun. If the first result is good, acknowledge that and use the explicitly labelled teaching example for critique.

## Case 2

The [walkthrough](../reference-products/case2/WALKTHROUGH.md) contains runnable prompts, expected values and the A–D presets. The [historical test report](../reference-products/case2/TEST_REPORT.md) distinguishes offline checks from actual model calls.

Use [context_messages.md](../data/case2/ground-truth/context_messages.md) to reveal context progressively. Baseline checks include CASE-001 = 68 units, CASE-005 = 13, and missing inputs remaining visible. After reviewed wholesale exclusions, CASE-013 changes from forecast 72.9/order 49 to forecast 28.17/order 0. Member Day context changes CASE-033 from order 155 to 2; clearance changes CASE-063 from 233 to 0. CASE-002's two-day shipment delay leaves the suggested order at 10 but creates one day with 10 unmet units.

The copilot works alongside the user. It proposes scoped changes and explains tool results; the user reviews and applies them. Verify saved context through a new request, not merely the previous chat answer. Keep raw observations intact and keep numerical calculations in the program.

The future week is synthetic validation evidence. It is not available to the initial build or runtime tools. A better forecast is not a guarantee of perfect prediction or a production performance claim.
