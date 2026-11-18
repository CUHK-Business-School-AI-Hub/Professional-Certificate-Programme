---
name: product-intelligence
description: Research new products and model changes for a specified brand, category or product family; trace discovery leads to original evidence and produce a verifiable product-intelligence report. Use for brand monitoring, latest-model checks and accessory-opportunity research.
---

# Product Intelligence

Run inside the host agent using its search, browser and document-reading tools. Read [rules.md](rules.md) before researching. No separate application or API key is required.

## Delegate: establish the brief

Resolve the requested brand and scope from official sources. Preserve a category or product-family restriction. For a whole brand, survey its categories rather than choosing one popular product. When a term such as “Hi-Fi” has multiple plausible meanings, state the interpretation and distinguish the relevant categories instead of silently substituting a mainstream flagship.

Use the five-element brief: **Goal, Facts, Examples, Standards, Boundaries**. Infer routine defaults and proceed: use the user's current date and timezone; start with the last 180 days; discover across accessible official markets and label each market. If no genuine new model falls in that window, expand to one year and then the latest verifiable release. A new colour or sale does not prevent this fallback. State the actual scope and whether this is a first snapshot or a comparison with accessible earlier records.

Default to one research run. Only create a recurring task when explicitly requested, using the host's scheduling capability. A list of rules or a schedule written in Markdown is not a running monitor.

## Execute with the domain rules

Use public discussions and media to discover leads, then trace them to official announcements, product pages and primary documents. Cross-check the official category/news index to catch products that received little discussion. Apply the source, identity, date and dimensions rules in `rules.md`.

Build a source register as you work: URL/domain, publisher, role (discovery / primary verification / document archive), what it supports, access status and any original source it points to. This is a task-specific source allowlist, not a fixed list of permitted brands. Follow new original-source links, verify ownership and add them to the register. Honour an explicit user restriction to named sites.

For each candidate, open the evidence and record product identity, market, event type, dates, known facts and missing information. Keep confirmed products separate from announced-but-unreleased products and unverified leads. Search snippets are leads, not opened primary evidence.

Complete one discovery pass across applicable channels and one targeted follow-up for model identity, dates, missing specifications and newer variants. Follow strong primary leads further when useful. After two failed approaches to a source, record the access limitation and use other evidence. Report uncovered categories explicitly instead of calling a partial scan exhaustive.

## Evaluate: deliver an inspectable result

Write the report, source register, tables, explanations and open questions in English by default, even when the request is in another language. Use a different output language only when the user explicitly requests it. Preserve official product names and model codes; translate source facts into English without changing their meaning. Start with the latest findings and their practical limits, then provide:

1. **Scope:** original request, resolved brand/category, cutoff date, markets, time window and comparison baseline.
2. **Confirmed findings:** product/model; category/market; event type; announcement and sale dates separately; key change; primary evidence links. Separate new hardware, local releases, editions/colours, bundles and software updates.
3. **Physical details where relevant:** dimensions with units, measured object, configuration and exact source. For cases and fit, distinguish housing, packaging, charging case, stand and folded/unfolded states. State missing measurements.
4. **Announced products and leads:** what the source actually establishes, what remains unknown, and the next check. A scheduled date having passed does not prove availability.
5. **Coverage and gaps:** sources actually read, index-only checks, blocked pages, inapplicable channels and unfinished checks. Use “latest found in this run,” not a guarantee of global completeness.

Check claims against sources, deduplicate copied announcements and inspect contradictions. Give a user an original link or a reproducible database query and record ID to check each material conclusion. Save the report and register only when requested or when an output location is part of the task; keep run data outside the installed skill.

## Coach: make a correction reusable

When the user identifies a failure, preserve the original finding and evidence. Diagnose whether it arose from missing facts, procedure or tool access. Propose a narrow revision to `rules.md`, explain which failure it addresses and apply it when editing is authorised. Present the rule change for human inspection; do not claim it was human-approved without an actual response.

Recheck the original input against the same criteria and, when available, the same source snapshot. Live-web reruns may contain new information, so identify that confound. Inspect at least one previously correct finding for regression, then try a new lead to test reuse. Record the revised rule, evidence and remaining gaps. Keep the success standard stable.

If no network tool is available, report that current monitoring cannot be performed. Analyse supplied material as a dated source review rather than inventing live findings.
