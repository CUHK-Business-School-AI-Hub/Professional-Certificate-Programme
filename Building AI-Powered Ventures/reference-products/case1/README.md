# Case One reference product

This is a reusable product-intelligence workflow run inside Codex. It uses the host agent's web tools; it is not a separate app and does not need a model API key.

## Open and run

1. Extract [product-intelligence.zip](product-intelligence.zip). Keep `SKILL.md`, `rules.md` and `agents/openai.yaml` together inside the `product-intelligence` folder.
2. Open a separate working folder in Codex. Point the agent to the extracted `product-intelligence/SKILL.md` and ask it to read `rules.md` before starting. Installing the skill globally is optional; reading the supplied skill directly is sufficient for this exercise.
3. Specify the brand/category, market and time window. Ask the agent to save the report and source register in the working folder, outside the skill.
4. Open the original sources, check the results, then record a confirmed correction and rerun with the same scope.

Example prompt:

> Read the supplied product-intelligence/SKILL.md and rules.md. Research new products from Dyson across all its product categories, covering the last 180 days as of today. Label each market and distinguish announcements from confirmed availability. Save report.md and sources.csv in this working folder. Include product identity, event dates, evidence, case-relevant dimensions and remaining gaps. Do not schedule recurring work.

Other classroom scopes are Sony's latest hi-fi headphones and the latest Nintendo Switch 2 Pro Controller. Clarify what “hi-fi” covers and distinguish Nintendo-made controllers from licensed third-party products. A new run needs current evidence; the skill itself is not evidence that a product is new.

## Reference output and evaluation

[The worked source-review example](examples/sony-mdr-m1.md) demonstrates an independently checked announcement date and explicit limits. It is a dated teaching example, not a current brand-wide monitoring report. Previous full three-case research reports are not present in this cleaned package and are not represented as delivered files.

Use slides 50–58 and the [Instructor Outline](../../notes/Instructor%20Outline.md) for the classroom loop. Learners attempt the task before receiving this reference skill. Preserve the first result; review the change to `rules.md`; reload the rules; then repeat the original task and inspect a previously correct finding.

## Maintainer entry points

- `product-intelligence/SKILL.md`: workflow, scope and output contract.
- `product-intelligence/rules.md`: reusable domain rules. Keep dated findings out of this file.
- `examples/sony-mdr-m1.md`: the worked source-review example and its primary source.
- Run `python3 assets/build_support.py` from the course directory after editing the skill to rebuild its ZIP. The installed skill in a personal agent's home directory is separate from this course copy.
