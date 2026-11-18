# Course source assets and build entry points

The folders here support the delivered course materials; students do not need them to open the slides or run a reference product.

| Location | What to edit |
|---|---|
| `case-one/` | Original visuals and provenance; slide text for pages 1–58 lives in the HTML deck. |
| `slide-images/` | Original image files recovered from embedded slide media. The HTML retains embedded copies for portability. |
| `case-two/build_slides.py`, `case-two/style.css` | Authoritative text, diagrams and layout for slides 59–83. |
| `api-access-guide/build_guide.py` | Four-page illustrated API guide; `openai-api-keys.webp` is its official illustration. |
| `data-generation/` | Seeded synthetic-data generation, verification, workbook export and packaging. |
| `build_support.py` | Generated speaker notes for slides 45–83 and shareable reference ZIPs; `--notes-only` regenerates just the notes. |
| `export_slides.cjs` | Slide PDF export and browser checks. |
| `verify_package.py` | Local links, data/package integrity and distribution boundaries. |

Run commands from the course root. Python 3.10+ handles the app, packaging and data checks. The API PDF builder needs ReportLab. Slide PDF export needs Node, Playwright and Chrome. Workbook rebuilding additionally needs `@oai/artifact-tool`; use the Codex workspace dependency loader to locate bundled runtimes, without hardcoding a cache version into source files.

Keep all preview images and logs in the repository's ignored `build/ventures-package/`. `NODE_PATH`, `CHROME_BIN` and `COURSE_QA_DIR` can point to the available runtime and scratch directory. Do not overwrite data merely to regenerate a ZIP: the supplied CSVs and fixed snapshot are the classroom baseline.
