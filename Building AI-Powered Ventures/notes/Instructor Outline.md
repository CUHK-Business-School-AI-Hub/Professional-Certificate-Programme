# Building AI-Powered Ventures

## Instructor outline · Slides 45–83 · English

These notes cover the two Day 1 afternoon cases, from 13:30 to 17:30. Apply the established Delegate → Evaluate → Coach methodology throughout; the morning lecture and Day 2 are outside the scope of these notes.

**Learning outcome.** Build and improve a product-intelligence workflow in Codex, then develop a rule-based replenishment dashboard and add a copilot through the model API. Both cases use simplified teaching scenarios; the inventory exercise uses synthetic data.

## Day 1 afternoon · From a Codex workflow to an AI-powered product

The afternoon follows three forms of work: a competitor-monitoring workflow operated inside Codex; a standalone replenishment dashboard that runs without an LLM; and the same dashboard with an embedded AI copilot. The monitoring workflow may use an LLM on each run. The distinction is between delegating work inside Codex and providing AI capabilities to users through a product.

### 13:30–14:30 · Hands-on: Build a Competitor Monitoring Workflow

**Learning outcome.** Use the morning’s five-element brief and Delegate → Evaluate → Coach loop to produce a verified product-intelligence report and a reusable workflow inside Codex.

**Business scenario.** Ask learners to imagine that they run a cross-border e-commerce business selling protective cases for products made by other brands. They need to discover product developments early enough to decide which devices their next cases should fit. Limit the first run to one brand or product series, a specified market and time window, and one product lead. Address learners as the business owners throughout the exercise: they decide which leads merit further investigation; the agent searches, follows sources, checks claims and organises the evidence.

The scenario and verification examples were adapted from sections 1.2 and 2 of 《向泰勒制告别：智能体原生企业的新范式》; the reading is background, not a prerequisite for running this package. The scenario and source method are already presented in slides 45–54. Keep the teaching method anchored in the established context, five-element brief, evaluation, coaching and reuse framework.

Slides 50–58 show the full classroom loop: an ordinary first request; agreed standards; a preserved first result; evaluation of gaps; domain-knowledge coaching; an agent-written `rules.md`; human review; a rerun; and learner practice on a new case. The first attempt uses a fresh exercise workspace. The deliberately incomplete report on slide 53 is labelled as a teaching example; actual test findings on slides 56–57 are separately identified. Slide 58 asks learners to choose Dyson across the whole brand, Sony Hi-Fi headphones, or the latest Nintendo Switch 2 Pro Controller, then run their own improved workflow. It supplies no findings or links to the prepared test answers.

Preparation and runnable materials: [Case One guide and prompt](../reference-products/case1/README.md), [product-intelligence skill](../reference-products/case1/product-intelligence/SKILL.md), [domain rules](../reference-products/case1/product-intelligence/rules.md) and [worked source-review example](../reference-products/case1/examples/sony-mdr-m1.md). The package contains the reusable reference workflow and a dated source check; it does not contain the earlier complete three-case run reports.

The package supplies source links in the slide notes and one worked source-review example. Prior product records and a saved web snapshot are optional, not assumed to exist. For a fresh run, state “first snapshot”; save the sources actually read during that run before coaching. If live pages change, record the changed evidence rather than attributing it to improved rules. Use a second lead to test reuse. Each monitoring run is learner-initiated. Keep reference findings as instructor material; release the reference skill after the exercise.

#### 13:30–13:40 · Define the Outcome and Success Standard

Slides 45–49 introduce the case: Product Intelligence; Their New Product. Your Next Opportunity.; Finding Out Earlier Gives You More Time.; The Information Is Scattered.; Let the Agent Track. You Decide What Matters. Introduce the scenario with “Suppose you run a cross-border e-commerce business selling protective cases like these.” Use the product and accessory images as illustrations, and the linked 2024 source examples to explain discovery and verification. The final page introduces the report structure and the learner’s decision-making role.

Use slide 49’s report structure to explain the business decision the report supports. Do not reveal the completed reference skill before the first attempt. Connect the learner’s role to slide 37: define success, resolve ambiguity and decide whether the result is ready for use.

Agree what counts as a useful finding before delegating: a clearly identified product, relevant dates and market, confirmed public specifications, original source links, new information relative to existing records and explicit open questions. Treat an earlier report as a format example; refresh the facts for the current run.

#### 13:40–13:55 · Delegate: Write the Brief and Prepare the Context

Apply the five elements from slide 33 to the monitoring task:

| Brief element | Monitoring example |
|---|---|
| Goal | Prepare a concise product-intelligence report that helps the operator decide which lead to investigate. |
| Facts | Specify the brand or series, market and time window; provide existing product records if available; otherwise label the run as a first snapshot. Search and browse to obtain current evidence. |
| Examples | Supply an earlier report for its organisation and level of detail. Keep its old product facts separate from current evidence. |
| Standards | Match claims to their sources; distinguish publication and launch dates; keep models, regions and units consistent; identify what is new and what remains unconfirmed. Retain the report and checking evidence. |
| Boundaries | Ask when essential scope is missing, flag inaccessible or conflicting sources, and stop at a report ready for review. The learner decides whether to pursue an opportunity. |

Codex may ask questions to fill gaps before execution. Save the confirmed brief and relevant references in the project, and explicitly have the agent read them. Apply slide 41’s completeness check: could a new collaborator proceed from these materials alone and return inspectable evidence? Use slides 50–52 to make the first attempt with a business goal and acceptance criteria. Introduce specialist source-finding procedures only during coaching, once the first result has been inspected.

Delegate the complete task: discover a lead, trace the original source, compare with known records, prepare the report and perform the agreed self-checks. Observe selected search, browse and file-writing actions as examples of the run loop from slide 22.

#### 13:55–14:15 · Evaluate: Inspect the Report and Evidence

Use slide 42’s four evaluation components:

| Component | Classroom check |
|---|---|
| Factual checks | Check that required fields and source links are present and that model identifiers, dates, markets and units match the cited material. Automate simple presence and consistency checks where useful. |
| Agent assessment | Have the agent inspect whether the sources support each conclusion, whether reposts describe the same underlying announcement, and whether an old product has been mistaken for a new launch. |
| Fair comparison | Save the initial report, source set and evaluation criteria. Keep these inputs and standards fixed when testing the coaching change. |
| Human review | Open the original sources and independently verify the findings that matter to the decision. Record passes, failures and unresolved gaps. |

Distinctly record “no new information found,” “source unavailable” and “claim unconfirmed.” A well-presented report is ready only when its claims pass the agreed checks. The learner accepts the report and decides what to investigate next.

#### 14:15–14:30 · Coach: Diagnose, Revise, Recheck and Reuse

Apply the sequence from slide 43. Use a failure found in the run, or a clearly labelled prepared example such as a repost date mistaken for a product launch date.

Introduce the instructor’s domain knowledge on slide 54: use social and forum discussions to discover leads, trace original announcements, search exact-model manuals, and check public FCC records for relevant wireless products. Manuals+ is a document-discovery channel; seek the manufacturer's original. Trace useful accounts to stable upstream sources and maintain a source register with distinct discovery and verification roles. Human experience and discussion with an LLM can both suggest improvements; verify the proposed method against the observed gap.

1. **Diagnose.** Preserve the original claim and evidence; identify whether the cause is missing facts, an incomplete procedure or a tool failure.
2. **Guide.** Write a specific reusable correction, such as tracing the original announcement and recording publication date separately from launch date.
3. **Revise.** Ask the agent to write the reusable correction into `rules.md` and show the diff. The learner checks the rule’s meaning, scope, exceptions and relation to the failure before authorising the classroom rerun. Correct all affected claims in the report as part of that rerun.
4. **Recheck.** Rerun the same case against the same source set and standards. Inspect whether the original failure is fixed and whether previously correct findings still pass.

Then apply slide 44’s next-run principle: load the improved brief and checks, refresh the evidence for the second product lead, and test whether the procedure can be reused without repeating the original explanation. Keep the old and new procedure, correction evidence and open questions in the workspace. This makes Save → Load → Apply → Maintain and context compounding visible in an actual task.

Close with the slide 58 exercise: each learner chooses a case, runs the improved workflow, checks a source and shares one finding plus a gap or rule change. The instructor will upload the prepared `product-intelligence` skill separately as a reference answer. Skill packaging is not part of this slide sequence.

**Completion check.** The learner can show the five-element brief, the report with source evidence, the evaluation record, one diagnosed correction and the result of rechecking it. Another learner can use the saved materials to run the workflow on a new lead and judge the output against the same standard.

### 14:30–17:30 · Build an AI-Powered Inventory Product

**Learning outcome.** Build an independent replenishment dashboard from simulated data, verify its calculations, then add a chatbot copilot that helps users supply context, compare options and review recommendations.

**Slide sequence: 59–83.** Keep the same Delegate → Evaluate → Coach labels as the morning and Case One. Slides 59–70 introduce experience-based rules, build an ordinary dashboard with no LLM at runtime, evaluate its calculations and forecast, coach it to handle reviewed 3-sigma outliers, and rerun the checks. Slide 71 makes the two development stages explicit: a chatbot copilot works alongside the user, incorporating new knowledge and temporary updates, exploring options and supporting qualitative judgments. The user confirms changes and makes decisions. Slide 72 obtains and tests API access before introducing the LLM-supported version. Slides 73–75 delegate and check the new app; slide 76 introduces how users supply business context through its chatbot. Slides 77–81 continue this second loop: evaluate a remaining forecast gap, provide Member Day and clearance context, then verify revised recommendations and an inbound-delay scenario. Slides 82–83 close with independent practice and production integration. Detailed page mapping and numerical sources are in [Case Two source](../assets/case-two/README.md).

#### 14:30–14:45 · From a Business Problem to a Product Brief

Continue the learner-owned business scenario: you sell protective cases across borders and now need a weekly replenishment plan. Use the [student data](../data/case2/student-data/README.md): 200 SKUs, 13 complete weeks of sales, stock, lead time, safety-stock days and at most one outstanding inbound batch per SKU. Freeze the snapshot at 16 November 2026. Keep [instructor ground truth](../data/case2/ground-truth/README.md) separate until the relevant validation stage.

Use this classroom rule:

```text
Weighted weekly demand = 0.4*T-1 + 0.3*T-2 + 0.2*T-3 + 0.1*T-4
Daily forecast demand = weighted weekly demand / 7
Planning days = lead time + safety-stock days
Recommended replenishment quantity =
  ceil(max(0, daily forecast demand × planning days − current inventory − eligible inbound))
```

T-1 is the most recent complete week. Use one warehouse and one transport mode. Eligible inbound becomes saleable before the exclusive end of the planning period. Project inventory by day: receipts enter at the start of their date; sales are limited by available stock; unmet demand is recorded separately as lost sales; closing stock stays nonnegative. A new order arrives on the snapshot date plus its lead time. The aggregate order formula does not optimise timing or deduct projected lost sales, so display shortages separately. Have Codex help write the brief and acceptance checks.

#### 14:45–15:25 · Build a Rule-Based Replenishment Dashboard

Use Codex to implement the dashboard. Show weekly sales, weighted demand, the product list and recommended quantities. Filter products requiring attention, inspect the calculation for one SKU, and show a daily stock projection with receipt dates and shortages. Keep raw historical sales separate from later corrections and context.

The dashboard runs without an LLM. AI supports development, while ordinary code executes the agreed formula.

#### 15:25–15:40 · Verify the Dashboard

Check CASE-001: T-1 through T-4 are 91, 70, 63 and 56 units. Weighted weekly demand is 75.6 and daily demand 10.8; with 40 on hand, seven days of lead time, three safety-stock days and no inbound, recommend 68 units. Also check sufficient inventory, final rounding, zero sales and missing values.

Use the first Coach loop to investigate unusually high weeks. The instructor's fixed baseline uses T-13 through T-5 and sample standard deviation. Flag recent observations above mean + 3 sigma, then confirm the simulated wholesale cause. Exclude confirmed exceptional weeks and renormalise the remaining original time weights. Recheck these cases and normal controls against Stage B ground truth. Do not reveal Member Day and clearance facts yet.

Correct any failures, rerun the checks and retain a working version before introducing the model API.

For the later chatbot phase, reveal Member Day participants, two full event weeks and a 50% uplift; divide the relevant non-excluded sales by 1.5, with no event in the validation week (Stage C). Then reveal the effective clearance list, which forces new orders to zero while retaining demand estimates and existing inbound (Stage D). Compare with the corresponding instructor answers. The hidden actual week separates demand, stock-constrained sales and unmet demand, so a stockout is not mistaken for lower demand.

#### 15:40–16:00 · Claim API Credits and Make Your First API Call

Use slide 72 and the [illustrated English handout](../guides/API%20Access%20Guide.pdf) immediately before delegating chatbot development. Have Codex prepare a backend `.env` file and add it to `.gitignore`; learners enter `OPENAI_API_KEY` locally themselves. The key stays out of chat and frontend code. The handout gives DeepSeek as an alternative when the Pro benefit is unavailable. Complete one small API call before continuing.

Explain the three objects: an API lets the application call a model; an API key authenticates the request; API credits pay for usage. Distinguish the API balance from the learner’s signed-in Codex allowance.

The course assumes learners have an eligible paid ChatGPT Pro subscription for using Codex. Under the official benefit checked on 18 November 2026, the subscription must have been active for at least seven days before claiming API credits. Include this requirement in pre-course instructions and recheck the benefit before teaching. The first grant is prorated for the remaining billing period, and unused monthly credits expire at the end of that period.

Walk through the following steps:

1. Sign in with the account that owns the Pro subscription and open ChatGPT Settings → Billing.
2. Start the API credits claim flow, select the receiving API organization the learner owns and activate the benefit. Use the same email address for the ChatGPT and API accounts.
3. Open API Platform, confirm the balance in the linked organization, select the project and create an API key.
4. Configure the key as an environment variable for the local backend. Keep it out of frontend code and the code repository.
5. Run a minimal model request and inspect the response.

**Completion check.** The learner’s application receives a successful API response.

Teaching references: [API credits benefit](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions), [claiming API credits](https://developers.openai.com/api/docs/guides/chatgpt-api-credits) and [API quickstart](https://developers.openai.com/api/docs/quickstart). Recheck the current interface and eligibility before class.

#### 16:00–16:10 · Break / Setup Support

Break, with TA support for learners who still need help completing API setup.

#### 16:10–16:50 · Add an AI Copilot to Your Product

Delegate the second version: add a chatbot copilot that works with the user to interpret business context, compare options and propose scoped updates. The user confirms changes; the application then recalculates and explains the results. Connect its backend to the model API, current dashboard data and existing calculation function. Support these interactions:

| Capability | Example question | Expected behaviour |
|---|---|---|
| Context | “CASE-033 participated in Member Days on 2–8 and 9–15 November; sales were about 50% higher.” | Propose normalising those event weeks, retain raw sales, and recalculate after confirmation. |
| Explain | “Why does CASE-001 need 68 units?” | Cite the actual inputs, formula and result. |
| What-if analysis | “What if CASE-002’s inbound shipment is delayed two days?” | Change that batch’s available date from 19 to 21 November, keep new-order lead time unchanged, and show the quantity and shortage changes. |

Trace one request through the product: the user asks in the page; the backend calls the LLM; the LLM requests a data or calculation tool; the program returns the result; and the page displays the explanation and supporting data.

The LLM interprets the request and organises the answer. Ordinary code calculates the quantity using the same data and formula as the dashboard. What-if analysis first produces a preview; current parameters change only when the user chooses to apply it.

#### 16:50–17:15 · Test, Evaluate, and Improve

Use a common set of checks:

| Test | What to inspect |
|---|---|
| A question with a known answer | Products and quantities match the dashboard. |
| A changed condition | A two-day delay to CASE-002’s existing inbound invokes the calculation tool: the order stays at 10 units while a one-day, 10-unit shortage appears. |
| Missing information | A question about an unspecified supplier lead time produces a clear statement of what is missing. |
| API failure | The interface reports the failure clearly, and the ordinary dashboard remains usable. |

Continue the second Delegate → Evaluate → Coach loop through the running product. Evaluate CASE-033 against the hidden next-week demand, then provide Member Day context through the chatbot and check the revised recommendation. Add the dated clearance decision for CASE-063 and verify zero new orders while demand and existing inbound remain visible. Check that context persists, unaffected SKUs remain correct, and a shipment delay changes only the intended batch. Finish with CASE-061, CASE-003 and CASE-196 as independent practice. If an implementation fault appears, repair and recheck it without introducing a separate teaching loop.

#### 17:15–17:30 · From Classroom Prototype to Production

Compare the classroom prototype with a production system:

| Classroom prototype | Production environment |
|---|---|
| Local simulated data | ERP, WMS or enterprise database records |
| Manually loaded data | Updates through backend services, controlled APIs or data pipelines |
| A simplified formula | Business-approved rules with maintenance and version control |
| Local trial use | User permissions, run records, error handling and ongoing maintenance |

Explain that real inventory systems typically connect to enterprise data through backend services or controlled APIs. Before production use, work with IT and data teams to confirm sources, field definitions, update frequency, access permissions and the scope of write-back. Confirm replenishment rules with the business owner. Keep model keys and database credentials on the server side.

Close by asking learners to choose a concrete user and problem for their own project, define the smallest demonstrable result, identify the required data and explain how they will verify it.
