# Case Two slide source

Slides **59–83** in `../../slides/AI-Ventures-202612-Slides-1.html` continue the existing English deck. The established 1600 × 900 canvas, typography, background, logo placement and teal/red accents are retained.

Keep all slide text in English. Bottom notes are optional and should add a necessary rule or action, rather than repeat the page. Slide 62 writes the forecast equation explicitly and defines each past-week sales variable using subscripts; the history-chart labels use the same notation.

Do not display source, snapshot or download annotations in the small footer area. Keep the page number. References remain in speaker notes and supporting documents.

## Authoring

Edit `build_slides.py` for the page content and native SVG illustrations, and `style.css` for Case Two layout. Run:

```sh
python3 "Building AI-Powered Ventures/assets/case-two/build_slides.py"
```

The builder replaces only the marked Case Two CSS and slide blocks, updates the initial page count, and writes `slide-map.json`. Earlier slides remain outside the managed blocks. The course HTML embeds the school logo and all diagrams, with local links to the student package and API handout.

## Teaching sequence

Two versions form the main narrative: first build a rule-based app that runs without an LLM; then obtain API access and build an LLM-supported version that supports the user through a chatbot copilot. Use Delegate → Evaluate → Coach in both parts. The second part continues the same loop through campaign, clearance and shipment scenarios.

| Pages | Purpose | Loop |
|---|---|---|
| 59–64 | Business scenario, weekly inputs, recency weights, inbound eligibility and daily stock | Introduce and agree the task |
| 65–66 | Five-element brief and first application build | Loop 1: Delegate |
| 67–68 | Known-answer checks and a next-week demand gap | Loop 1: Evaluate |
| 69–70 | Confirm a wholesale event, update rules, inspect and rerun | Loop 1: Coach, then Evaluate |
| 71 | Explain the two development stages and how a chatbot copilot works alongside the user | Transition to Stage 2 |
| 72 | Claim Pro API credits, create a key, store it in backend `.env`, test once | Preparation before the chatbot |
| 73–74 | Delegate a bounded chat feature and inspect the model/tool design | Loop 2: Delegate |
| 75–76 | Check the new app and introduce how to supply scoped business context | Loop 2: Evaluate, then prepare to Coach |
| 77–79 | Request the next plan, inspect a remaining gap, add Member Day context and re-evaluate | Loop 2: Evaluate → Coach → Evaluate |
| 80–81 | Apply a dated clearance policy and verify an inbound-delay scenario | Loop 2: Coach and Evaluate |
| 82–83 | Independent combined-case exercise and production data integration | Reuse the full loop |

## Methodology alignment

Use the morning framework as the standard: the five-element brief distinguishes examples from requirements; evaluation uses independent evidence and retains the same comparison target; coaching records a confirmed correction and tests its reuse. The Stage 1 forecast correction is still compared with the same 27-unit next-week demand. An outlier flag is a reason to investigate, not proof of a wholesale order.

In Stage 2, the chatbot serves as a copilot working alongside the user. The user supplies context, explores options and confirms changes; the copilot interprets context, suggests adjustments and explains results. Tool use supports this collaboration, while ordinary code calculates quantities. Review changes before applying them, save confirmed context, and reload it for a new request. Keep reusable methods separate from dated business events. Slides 73, 78, 79 and 82 make these steps explicit.

## Numerical evidence

The charts and reference values come from `../../data/case2/student-data/` and `../../data/case2/ground-truth/`. They are synthetic reference expectations, not screenshots or claimed results of an implemented student app.

- CASE-001: weekly weighted demand 75.6, daily demand 10.8, order 68.
- CASE-013: stage A demand 72.9 and order 49; stage B demand 28.166667 and order 0. The recent 140-unit week exceeds the older-nine-week upper 3-sigma line of 43.945219.
- CASE-033: no 3-sigma flag. Stage B demand 132.8 and order 155; Member Day normalisation changes these to 98.4 and 2. Raw event-week sales remain 150 and 144.
- CASE-063: clearance changes the new order from 233 to 0; demand is retained.
- CASE-002: both ten-day curves include the proposed 10-unit order on 23 November. Moving the existing 50-unit shipment from 19 to 21 November leaves the order at 10 and creates 10 unmet units on 20 November. These curves are model projections; the hidden one-week actuals have a different horizon and exclude new student orders.

Ground truth should be revealed progressively. The combined CASE-061 answer is not printed on the independent-exercise page. No campaign or clearance answer is introduced before the API and chatbot section.

## API references

The API page links `../../guides/API Access Guide.pdf`. Claim and key-creation instructions were rechecked on 18 November 2026 against [OpenAI's credit-benefit guide](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions) and [project/API-key documentation](https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform). The handout includes DeepSeek as the alternative. Keys remain in a local backend environment file excluded from Git; no actual credential is included here.

Visual QA images and geometry reports are stored in the ignored `build/ai-ventures-case-two/` directory.
