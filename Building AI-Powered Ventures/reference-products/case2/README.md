# Case 2 · Inventory Studio reference answer

A runnable local reference for the Case Two hands-on slides (59–83): a deterministic replenishment dashboard with an OpenAI-powered copilot. The interface and teaching prompts are in English; the chatbot follows the language of the question. This is an instructor reference containing staged answers.

## Start

For a standalone copy, download [case2-reference.zip](../case2-reference.zip), extract it and open the `case2` directory. The ZIP includes synthetic inputs and instructor test data, but excludes API keys, local state and caches. Inside the course workspace, the app reads shared data from `../../data/case2/`.

On macOS you can also double-click `start.command` to launch the local server.

Requires Python 3.10+; no third-party Python or Node packages are needed. From this directory:

```sh
python3 server.py
```

Open [the local app](http://127.0.0.1:8765). From the repository root:

```sh
python3 "Building AI-Powered Ventures/reference-products/case2/server.py"
```

The server binds to `127.0.0.1`, serves only three allowlisted frontend files and API routes, and supports one shared local classroom state. Use `--port 8766` if the default port is occupied. Stop with Ctrl+C. This reference stays local; it has not been deployed to Sites hosting.

## API setup

The ordinary dashboard works without an API key. The backend reads `OPENAI_API_KEY` and optional `OPENAI_MODEL` from environment variables or this directory's `.env`. Existing standalone-key files are also accepted. Environment variables take precedence. Files are read on each request.

For a fresh installation, copy `.env.example` to `.env` and fill it locally. Default model: `gpt-4.1-mini`. Actual chatbot requests use the paid OpenAI API. The browser never receives the key. `.env` and local state are ignored by Git. Do not include them when sharing the app.

“Key configured” means only that a key was found. “API connected” appears after a successful real request. On macOS, if Python lacks its own CA bundle, the app uses `/etc/ssl/cert.pem` with certificate and hostname verification enabled. A custom trusted bundle can be supplied with `SSL_CERT_FILE`. Missing credentials, authentication failures, rate limits, missing credit, network failures and timeouts produce an error while the dashboard remains usable. No simulated reply is substituted for a failed model request.

Implementation follows the official [Responses API quickstart](https://developers.openai.com/api/docs/quickstart) and [function calling flow](https://developers.openai.com/api/docs/guides/function-calling). `store: false` is used for model requests. The request contains the user's question, recent chat messages, tool definitions and relevant synthetic tool results.

## Use in class

Follow [WALKTHROUGH.md](WALKTHROUGH.md) for prompts, expected results and the Delegate → Evaluate → Coach sequence. Follow [TEST_REPORT.md](TEST_REPORT.md) for what has actually been tested.

- Search/filter all 200 SKUs, inspect the formula and 13-week raw sales, view daily stock/receipt/shortage ledgers, and export the current filtered plan as CSV.
- Ask queries and explanations through the assistant; expand **Evidence** to inspect tool arguments and returned data.
- Paste confirmed business context into the assistant. Review the proposed events and before/after results, then click **Apply reviewed change**.
- A–D buttons load instructor presets **as a preview**. They reset inbound overrides when applied. Use these to recover the exact baseline between demos, rather than revealing later answers before the corresponding lesson.
- The **Teaching tools** section exposes anomaly candidates and approved change history. Anomaly screening does not apply exclusions.
- Approved state survives restarting the server. Chat text is held in browser memory and clears on reload. Pending previews expire when the server restarts or any change is applied. Historical messages refer to their displayed version; new questions query the current version.

## Files and boundaries

| File | Purpose |
| --- | --- |
| `engine.py` | Independent calculation engine, historical sales and daily simulator |
| `service.py` | Read tools, validated previews, human apply, state versions and persistence |
| `chat.py` | Server-side Responses API calls, tool loop and model instructions |
| `server.py` | Local HTTP endpoints, static allowlist and same-origin write checks |
| `static/` | Buildless HTML, CSS and JavaScript |
| `rules.md` | Reusable calculation and review contract |
| `context/stage_B.json`, `stage_C.json`, `stage_D.json` | Instructor-approved business facts, sourced from the existing synthetic `business_events.csv`; cumulative presets, not expected orders |
| `tests/test_reference.py` | Deterministic calculations, tool loop, persistence and HTTP tests |
| `tests/evaluate_forecasts.py` | Offline next-week forecast evaluation |
| `tests/live_timing.py` | Focused live regression distinguishing the planning horizon from lead time |
| `tests/live_chat.py` | Explicit opt-in real model tests; isolated state; consumes API credits |

Runtime calculations do not load `expected_plans.csv`, future actuals, latent profiles or missing-value answers. The runtime uses the student CSVs and approved events; the testing code separately reads answer files. Source and student data stay unchanged. The five missing values remain explicit issues; automatic repair is outside this reference.

## Repeat the checks

From this directory:

```sh
python3 tests/test_reference.py
python3 tests/evaluate_forecasts.py
node --check static/app.js
```

The HTTP test needs permission to bind a temporary loopback port. Real chatbot evaluation additionally requires API access and permission to send the synthetic case data:

```sh
python3 tests/live_chat.py --run --output "local-state/qa/live-results.json"
```

For the additional planning-horizon wording regression, run `python3 tests/live_timing.py --run --output "local-state/qa/live-timing.json"`.

The live test sends the existing synthetic Member Day and clearance reveal texts, checks model tool selection and returned results, and records answers plus tool traces. It uses an in-memory `Service`, so the browser's saved state is unaffected. Review generated natural-language answers as well as automated assertions. Do not describe mocked transport tests as real model tests.
