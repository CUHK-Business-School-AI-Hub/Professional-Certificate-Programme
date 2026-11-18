# Day 1 case notes · Slides 45–83

Instructor-only companion covering slides 45–83, generated from the HTML speaker notes. Morning lecture notes and Day 2 are excluded. Edit the HTML for Case One, or `assets/case-two/build_slides.py` for Case Two, then regenerate this file. The [Instructor Outline](Instructor%20Outline.md) is the teaching plan. Do not distribute these notes before the exercises.

## Slide 45 · Product Intelligence

Begin the one-hour hands-on with the management loop from slides 40–44. Learners will operate a monitoring workflow inside Codex. Invite learners to imagine running a cross-border e-commerce business that sells protective cases for other brands’ devices.
Sources: Illustrative product image: [Dyson](https://www.dyson.com/hair-care/hair-stylers/airwrap-id/straight-wavy-ceramic-pink-rose-gold).

## Slide 46 · Their New Product. Your Next Opportunity.

Address learners as the business owners: suppose you run a cross-border e-commerce business selling protective cases like these. Which devices should your next cases fit? The Dyson product and case illustrate the scenario; no actual learner business or brand affiliation is implied.
Sources: Illustrative product and case. Images: [Dyson product](https://www.dyson.com/discover/news/latest/introducing-dyson-airwrap-id-multi-styler-and-dryer) · [Dyson case](https://www.dyson.com/support/journey/spare-details.974498-06).

## Slide 47 · Finding Out Earlier Gives You More Time.

Walk through the stages without assigning invented lead times. Finding a lead starts evaluation; it does not establish that the opportunity is viable. Development, production, shipment and listing still require work and human decisions.

## Slide 48 · The Information Is Scattered.

These are reformatted source excerpts with an actual manual-page image, not live website screenshots. Use them to distinguish discovery from verification. A recent report may concern an older product; a publication date is not automatically a launch date. Follow reposts to original evidence and keep product models and markets separate. The historical example is from 2024, not a current-new-product claim.
Sources: Historical source examples (2024), reformatted for teaching: [Dyson article](https://www.dyson.com/discover/news/latest/introducing-dyson-airwrap-id-multi-styler-and-dryer) · [Reddit thread](https://www.reddit.com/r/Dysonairwrap/comments/1et3ebx) · [Dyson manual](https://www.dyson.com/content/dam/dyson/maintenance/user-guides/en_US/personalcare/dysonairwrapstyler/AirwrapID-User-Manual.pdf).

## Slide 49 · Let the Agent Track. You Decide What Matters.

The learner remains the AI manager: define the goal and standard, review evidence and decide whether a lead merits further investigation. The agent collects and checks information. Next, write the five-element brief: Goal, Facts, Examples, Standards and Boundaries. This page introduces the deliverable; it does not replace the morning’s management method.

## Slide 50 · Delegate: Start with Your Goal

Use a fresh exercise workspace. Do not invoke the mature product-intelligence skill before this first attempt. Choose a brand, market and time window; ask for missing essential scope. This is an intentionally ordinary delegation, not a command to produce a bad answer. Establish the standards on the next slide before executing.

## Slide 51 · Agree on What “Good” Means

Connect to the five-element brief from slide 33: Goal is the report and decision; Facts are brand, market and window; Examples are optional report formats; Standards are the checks on this slide; Boundaries require explicit unknowns and human opportunity decisions. Learners need not know expert search procedures to define success.

## Slide 52 · Run Once. Keep the Evidence.

The filenames are classroom examples. Save the scope and source snapshot with the first result. Observe tools being used, but do not micromanage every action. The learner reviews evidence rather than accepting the agent’s self-assessment.

## Slide 53 · Evaluate: What Is Missing?

This report is a deliberately incomplete teaching example, not an actual test output. Prefer a real gap from the learner’s first run. If it already meets the standard, acknowledge that success and use this example for the critique exercise; do not claim every first run fails. Record passes, failures and unresolved questions.

## Slide 54 · Coach with Domain Knowledge

The domain method comes from the instructor’s production experience. Domain knowledge may also emerge through discussion with an LLM, but proposed sources and procedures still need verification. Maintain source roles and a task-specific source allowlist; it can grow when a new original source is verified. Do not present private reasoning or a hidden chain of thought.
Sources: Source methods: [Manuals+](https://manuals.plus/) · [FCC public search](https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm).

## Slide 55 · Turn Feedback into rules.md

This is a concise teaching excerpt, not the entire skill. The actual rules.md is in reference-products/case1/product-intelligence. Have the agent preserve the original report and present its rule changes for the learner to inspect before the classroom rerun. Keep per-run brand, date and findings outside reusable rules.

## Slide 56 · You Review the Rule Change

The added rule is based on the actual 17 November 2026 research: a CameraJet page contains “273 m”, and a Nintendo product page has a conflicting battery value. The supplied skill is version 1.1 with a saved v1.0 and diff. Human review is pending until the user or learner actually inspects it; the slide does not claim that approval has occurred.

## Slide 57 · Rerun. Keep the Standard.

Use the original source snapshot for a controlled classroom comparison. If using live pages, record changed sources as a confound. The real check is from the skill run: Sony’s original announcement established the 2024 date independently of newer indexed or exported documents. This is a source-verification example, not a fabricated A/B performance result.
Sources: Evidence: [Sony MDR-M1 original announcement](https://www.sony.eu/presscentre/sony-launches-closed-monitor-headphones-with-high-sound-isolation-for-studio-sound-quality-anywhere).

## Slide 58 · Try the Rules on a New Case

Invite learners to choose one of the three cases and run their own workflow using the rules they have improved. They should define any missing scope, inspect a source and share one finding plus a gap or rule change. Keep the prior test reports out of the exercise prompt. The instructor will upload the prepared skill separately as a reference answer; no skill-packaging demonstration is included here.

## Slide 59 · Replenishment Dashboard

Continue the learner-owned protective-case business. Build and evaluate the ordinary program before adding the API-connected chatbot. Use Delegate, Evaluate, Coach throughout. The illustration does not claim an implemented dashboard.

## Slide 60 · What Should You Reorder?

Do not introduce wholesale, campaign or clearance answers yet. Ask what decisions the dashboard should support. The learner owns the purpose and acceptance criteria. Teaching reminder: Delegate a usable weekly decision tool. Define how you will check it.

## Slide 61 · Start with Two Data Files

Use student-data.zip only. Missing required fields must produce a specific data issue. No historical daily sales are supplied. Later daily demand values are forecasts. Instructor truth stays separate until the evaluation stage.
Sources: Download: [Student data package](../data/case2/student-data.zip) · 200 SKUs / 2,600 weekly records

## Slide 62 · Give Recent Sales More Weight

The coefficients are a rule drawn from operating experience. Each T with a negative subscript denotes units sold in a past complete week, not subtraction from T. The most recent completed week receives weight 0.4. The four weights sum to one. This is a weekly forecast; divide by seven for the uniform daily forecast used in this exercise.
Sources: Synthetic classroom data · Snapshot: 16 Nov 2026

## Slide 63 · Calculate the Replenishment Quantity

Eligibility is as_of_date <= available_date < as_of_date + coverage_days. Current stock excludes inbound. The aggregate rule plans full forecast demand without optimising timing or deducting expected lost sales. It does not guarantee absence of stockout.

## Slide 64 · Check When Stock Will Be Available

The curve includes the proposed ten-unit order. A seven-day lead time from 16 November means availability on 23 November. Sales=min(available,demand); closing stock=available-sales; unmet demand=demand-sales and is lost, not backordered. Chart points are day-end stock.
Sources: Synthetic classroom data · Snapshot: 16 Nov 2026

## Slide 65 · Delegate: Define the First Version

Use the five elements from slide 33. The completeness check from slide 41 includes outcome, context, quality, evidence and boundary. Save the confirmed brief. Ordinary development tools are enough; no model API is needed yet. Teaching reminder: Ask for a working page, calculation evidence and a short run guide.

## Slide 66 · Build the First Version

This is a layout sketch, not an implemented product screenshot. Learners have Codex build and run the app, inspect its actual screen and preserve the initial calculation output for a fair comparison. Teaching reminder: AI helps build the program. The dashboard runs without an LLM.

## Slide 67 · Evaluate: Does the App Calculate Correctly?

These are reference checks, not claims that an app has passed. CASE-005: 17/7*10−12=12.2857..., which rounds up to 13. Preserve these checks after changes. Teaching reminder: Check arithmetic, time units and missing-data behaviour.

## Slide 68 · Evaluate: Does the Forecast Make Sense?

Reveal this synthetic next-week comparison after the initial run has been saved. Compare forecast to customer_demand; stockouts can reduce realised sales. Do not let the original build read instructor files or disclose campaign and clearance facts yet. Teaching reminder: Find the cause of the gap before changing the rule.
Sources: Synthetic classroom data · Snapshot: 16 Nov 2026

## Slide 69 · Coach: Handle Exceptional Sales

Use T−13 through T−5 and sample SD with n−1. The high week must not raise its own baseline. Treat wholesale as a possible explanation, then review the flagged weeks before excluding them. The instructor event record supplies the confirmation for this simulation. Excluding T−1 leaves weights 0.3,0.2,0.1 summing to 0.6; retain their time positions and divide by 0.6. A flag alone is not proof of wholesale.

## Slide 70 · Evaluate: Rerun After Coaching

Stage B reference. CASE-013 becomes (0.3*28+0.2*29+0.1*27)/0.6=28.1667, not exactly the future demand of 27. Compare the actual app to these expectations. Save the failure, rule diff and recheck. This closes the first loop before the model API. Teaching reminder: Record what improved, what stayed correct and what remains unresolved.

## Slide 71 · Next Step: Add a chatbot as copilot

This is the transition between two development stages. Stage 1 uses AI to build ordinary software and completes a Delegate, Evaluate, Coach loop. Stage 2 adds an LLM-powered copilot that works alongside the user. The user supplies context, considers alternatives and confirms decisions; the copilot helps interpret information, propose adjustments and explain results. The existing calculator still computes quantities; proposed changes remain subject to review. Obtain API access on the next page before delegating this new version.

## Slide 72 · Get API Access for the Next Version

Use the same account email and an API organization the learner owns. The first grant can be prorated and monthly credits expire at cycle end. Create the key in that organization. This is setup between loops. Use the PDF for illustrated steps and the DeepSeek alternative. No key is embedded in this deck.
Sources: [Illustrated API Access Guide](../guides/API%20Access%20Guide.pdf) · [Official credit benefit](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions) · Checked 18 Nov 2026

## Slide 73 · Delegate: Build the Copilot

Five-element brief: goal=chat feature; facts=current dataset and calculator; examples=the existing dashboard and CASE-001 acceptance check; standards=correct SKU, source values and shared calculations; boundaries=preview before applying, preserve raw data, keep secrets backend-only. This is a development request to Codex. Later operating requests are made through the product. Teaching reminder: Return the working feature and evidence that each check passes.

## Slide 74 · What Changes at Runtime?

The LLM does not directly edit a browser or database here. The backend orchestrates model-tool interaction and executes allowed functions on current application state. Both interfaces use the same calculator. Ask the agent to trace one input through this design. Teaching reminder: The model requests actions. Your backend executes the tools.

## Slide 75 · Evaluate: Check the New App

Restore stock to 40 after the temporary change. Simulate API failure safely in the local exercise. Use independent arithmetic and inspect browser behaviour. A connection test alone does not prove feature correctness. Teaching reminder: Compare the answer, tool result and dashboard against the same inputs.

## Slide 76 · Share Context with the Copilot

This page introduces how a business owner works with the copilot by supplying additional context. The copilot supports human judgment; the user confirms changes and owns the decision. The LLM interprets a message and the backend proposes a scoped update. The user reviews it before it is saved and used by the calculation tools. Do not introduce a separate software-debugging loop here. If a real implementation fault occurs, fix and recheck it as needed, without diverting the teaching narrative.

## Slide 77 · Evaluate: What Is Missing from the Data?

The operational delegation in Loop 2 is to generate the next plan from current data and saved rules. Evaluate that plan, then coach the product with facts. Reveal this comparison before naming the campaign. The 3-sigma line is computed from the nine older weeks. Teaching reminder: A correct calculation can still lack important context.
Sources: Synthetic classroom data · Snapshot: 16 Nov 2026

## Slide 78 · Coach: Explain the Member Day Campaign

Events cover complete weeks with an assumed 1.5 multiplier. Divide by 1.5 rather than subtracting 50%. Preview affected rows and persist the event after confirmation. Keep earlier wholesale exclusions if both conditions affect one week. This is a teaching assumption to validate in production.

## Slide 79 · Evaluate: Check the Revised Recommendation

Reference stages B and C. Forecast 98.4 differs from actual demand 92; correction is not perfect prediction. Show an adjusted demand basis without rewriting the recorded sales. Check a new request or reload so the event persists beyond the previous chat turn. Teaching reminder: Reload the saved event and confirm the result is reproducible.

## Slide 80 · Coach: Explain a Clearance Decision

CASE-063 has a stage C order of 233 and stage D order of zero. Demand stays 70.2 units/week. Clearance changes the action, not forecast demand. Persist a dated SKU-specific decision and a general precedence rule. Do not cancel existing inbound. Use the original request and a normal control for the rerun. Teaching reminder: Re-evaluate: zero new orders for this SKU; normal rules for other SKUs.

## Slide 81 · Evaluate: Check an Inbound Delay

Reference from delay_scenarios.csv. Both curves include ten new units on 23 November. Existing fifty-unit shipment shifts from 19 to 21 November, staying inside the ten-day window. If the model changes new-order lead time or all SKUs, diagnose that scope error, coach it and rerun the same scenario.
Sources: Synthetic classroom data · Snapshot: 16 Nov 2026

## Slide 82 · Your Turn: Complete the Loop

Do not reveal the combined-case answer on the page. At this stage the instructor provides the relevant records. CASE-061 combines wholesale, Member Days and clearance. Grade against stage D and inspect rule priority. Require calculation evidence and persisted context. Teaching reminder: Demonstrate what changed and what stayed correct.

## Slide 83 · From Sample Data to Production

Production data comes through backend services, controlled APIs or approved pipelines. Keep database credentials and model keys on the server. Synthetic exercise results are not production accuracy evidence. Maintain confirmed rules and context as the business changes. Day 2 remains unchanged. Teaching reminder: Delegate clearly. Evaluate actual outcomes. Coach and retain the improvements.
