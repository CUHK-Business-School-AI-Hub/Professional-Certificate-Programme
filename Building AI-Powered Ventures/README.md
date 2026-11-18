# Building AI-Powered Ventures

**Innovation and Entrepreneurship in the Age of Generative AI** · PCP Course 1 · 2–3 December 2026 · CUHK Business School

## Philip 的讲师入口

下午让学员经营同一家跨境保护套电商，先判断哪款新设备值得开发保护套，再决定已有商品该补多少货。两个案例都让学员先委派任务，再用证据评价结果，把确认过的改进带入下一次运行。在本地仓库中用浏览器打开[第 45 页](slides/AI-Ventures-202612-Slides-1.html#slide-45)，备课时看[下午教学时间表](notes/Instructor%20Outline.md)。

| 时间及页码 | 课堂上做什么 | 打开什么 |
|---|---|---|
| 13:30–14:30 · 45–58 | 在 Codex 里先跑一次新品监控，让学员打开原始来源核查一条结论。把发现的问题写成规则，再用同一标准重跑。练习结束后发参考 skill。 | [Case 1 参考 workflow](reference-products/case1/README.md) |
| 14:30–15:40 · 59–70 | 只发学生数据，用经验公式做补货 dashboard。先手算核对，再揭示异常销量，请学员修订规则并比较前后结果。这一版可以离线运行。 | [学生数据 ZIP](data/case2/student-data.zip) · [讲师演示步骤](reference-products/case2/WALKTHROUGH.md) |
| 15:40–17:30 · 71–83 | 第 71 页讨论为什么需要 copilot，第 72 页设置 API。16:00–16:10 休息并协助配置。随后让学员提供会员日、清库存或到货延迟信息，审阅 copilot 的建议，确认后查看新计划。 | [API 图文指南](guides/API%20Access%20Guide.pdf) · [按阶段揭示的业务信息](data/case2/ground-truth/context_messages.md) |

补货参考应用中的 **A、B、C、D** 用来重现课堂上的四次计算。A 是原始公式，B 加入已确认的批发异常，C 再加入会员日，D 再加入清库存。A、B 用于第一版 dashboard 的演示，C、D 用于检查第二版 copilot 接收背景后的计算结果。

讲台上可按页查阅[下午逐页 notes（45–83 页）](notes/Slide%20Notes.md)。第二天的项目安排见 [syllabus](guides/Building%20AI%20Powered%20Ventures%20Syllabus.docx)。

### 材料索引

| 你要做什么 | 打开这里 |
|---|---|
| 上课 / 查看课件 | [Day 1 HTML](slides/AI-Ventures-202612-Slides-1.html) |
| 备课：第 45–83 页两个案例 | [Instructor Outline](notes/Instructor%20Outline.md)、[逐页讲师 notes](notes/Slide%20Notes.md)、[材料发放与演示顺序](notes/README.md) |
| 开始 Case 2 学生练习 | [学生数据 ZIP](data/case2/student-data.zip)；[字段与计算规则](data/case2/student-data/README.md) |
| 取得 Case 1 参考成品 | [产品情报 workflow / skill](reference-products/case1/README.md)、[可分享 skill ZIP](reference-products/case1/product-intelligence.zip) |
| 运行 Case 2 参考成品 | [补货 dashboard + copilot](reference-products/case2/README.md)、[独立运行包](reference-products/case2-reference.zip) |
| 查看课程要求和课前准备 | [Syllabus](guides/Building%20AI%20Powered%20Ventures%20Syllabus.docx)、[Pro API 额度图文指南](guides/API%20Access%20Guide.pdf)、[Codex 入门指南](guides/Codex%20Desktop%20Getting%20Started%20Guide.pdf) |
| 修改或重建材料 | [资产与制作入口](assets/README.md)，以及本 README 后半部分 |

### 课前准备

学员自行准备包含 Codex 使用权限的 **ChatGPT Pro** 付费订阅；这是本课程所说的“Codex Pro plan”。请在领取 API 额度前至少提前 7 天激活付费订阅。领取入口、关联 API organization、建立 key、保存 key 和最小调用测试见 [API Access Guide](guides/API%20Access%20Guide.pdf)。规则于 2026-11-18 按[官方说明](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions)核对；是否领取成功以个人账户里显示的额度为准。

Case 1 在 Codex 内运行；Case 2 的普通 dashboard 无需 API key。只有加入 copilot 后才需要模型 API。参考应用默认接 OpenAI；指南中的 DeepSeek 是备选服务，需要相应调整应用的 provider 集成，不能把它的 key 直接填进 `OPENAI_API_KEY`。

### 六类材料

```text
slides/                  第一天下午案例及上午原则：83 页 HTML
notes/                   仅第 45–83 页：案例大纲、逐页 notes、发放指南
data/case2/             学生模拟数据与讲师 ground truth（分别打包）
reference-products/
  case1/                 可复用 skill、规则、操作指南和一个带来源的示范输出
  case2/                 可运行的 dashboard + copilot 及测试
  case2-reference.zip    含模拟数据的独立参考应用包
guides/                 Syllabus、API 图文指南、Codex 入门指南
assets/                  图片、生成器、导出与检查工具
```

### 参考应用快速启动

Case 2 需要 Python 3.10+，基础功能不需要额外 Python 或 Node 包。打开 `reference-products/case2/`，运行 `python3 server.py`，或在 macOS 双击 `start.command`，然后打开 <http://127.0.0.1:8765>。API key 放在该目录的 `.env`，样例为 `.env.example`。

给学生分享时使用本目录各材料的独立 ZIP。它们不含本地 key、运行状态或缓存；请不要直接压缩自己的工作目录。完整参考应用 ZIP 含讲师数据和分阶段答案，应在对应练习结束后发放。

## 给 Philip 的 personal agent

Open the [Dec2 branch of the programme repository](https://github.com/CUHK-Business-School-AI-Hub/Professional-Certificate-Programme/tree/Dec2) and enter `Building AI-Powered Ventures/`. For your first briefing, record the commit you inspected and follow the links below. For later updates, compare that commit with the new revision of this course directory and report changes that affect Philip's teaching.

| What Philip needs to know | Where to check |
|---|---|
| How the afternoon runs | Read the [timed outline](notes/Instructor%20Outline.md) for slides 45–83. Use the [release order](notes/README.md) to identify when students get data, business context and reference answers. |
| What learners produce in Case 1 | Follow the [skill and worked example](reference-products/case1/README.md). Learners check a product claim against its source, revise their rules and repeat the task. |
| How the two builds differ in Case 2 | Follow the [walkthrough](reference-products/case2/WALKTHROUGH.md). The first dashboard executes a formula. Slides 71–73 introduce the copilot, set up API access and delegate the second build. The user reviews proposed changes before applying them. |
| Which figures to quote | Use the [existing simulation](data/case2/README.md). In [expected_plans.csv](data/case2/ground-truth/expected_plans.csv), compare CASE-033 at B and C for the individual order (155 to 2). The Stage C total of 115 SKUs requiring replenishment is for the full dataset after applying the [supplied promotion context](data/case2/ground-truth/context_messages.md) for all 32 participating SKUs. |
| What is required for the copilot | Link the [illustrated API guide](guides/API%20Access%20Guide.pdf). For past test results, cite the date and scope in the [test report](reference-products/case2/TEST_REPORT.md). |

Give Philip a short briefing in teaching order. For each case, name the student deliverable, the evidence learners will check, the material to release and its slide range. Link each point to the repository file you used. If a file is missing in the revision you inspected, identify the missing path. Reading the repository is sufficient for this briefing.

### Maintenance when requested

The deck uses English and a fixed 1600 × 900 canvas. Keep the approved Delegate → Evaluate → Coach terminology. The [slide map](assets/case-two/slide-map.json) identifies the Case 2 teaching step on each page.

### Source of truth

- Slides 1–58: edit `slides/AI-Ventures-202612-Slides-1.html` directly. Media is embedded; original image assets are retained under `assets/`.
- Slides 59–83: edit `assets/case-two/build_slides.py` and `style.css`, then run the builder. Direct edits inside managed blocks will be overwritten.
- `notes/Instructor Outline.md`: editable teaching plan for slides 45–83 only. `notes/Slide Notes.md`: generated only from slide 45 onwards; edit the slide source instead. Do not add morning-lecture or Day 2 notes. Use `python3 assets/build_support.py --notes-only` to regenerate notes without rebuilding reference ZIPs.
- `guides/Building AI Powered Ventures Syllabus.docx`: editable formal syllabus. Preserve approved dates, assessments and Day 2 arrangements unless asked to change them.
- `assets/api-access-guide/build_guide.py`: source of the illustrated API PDF. Recheck official eligibility and UI before teaching; a subscription is not proof of a credited API balance.
- `data/case2/student-data/*.csv` and `dataset.json`: fixed classroom inputs. Ground truth is instructor-only. CSVs are authoritative; Excel files are reading copies.
- `reference-products/case1/product-intelligence/`: course copy of the skill. Do not silently replace the user's installed personal copy.
- `reference-products/case2/`: runnable Python reference. Runtime reads student data and confirmed context, not future actuals or expected answers.

### Rebuild only what changed

For an authorised maintenance task, select the command for the affected deliverable and run it from this course directory. The packaging commands below are for explicit requests to refresh the existing student or reference archives.

```sh
python3 assets/case-two/build_slides.py
python3 assets/api-access-guide/build_guide.py
python3 assets/data-generation/verify_data.py
python3 assets/data-generation/package_data.py
python3 assets/build_support.py
node assets/export_slides.cjs
python3 assets/verify_package.py
```

The PDF builder needs ReportLab. Slide export needs Playwright and Chrome. In Codex, use `load_workspace_dependencies` to locate bundled Python, Node and package paths; set `NODE_PATH` and, if needed, `CHROME_BIN`. No API calls are made by these build commands.

Only regenerate raw data when deliberately changing the case: `python3 assets/data-generation/generate_data.py`. Then verify, run `node assets/data-generation/build_workbooks.mjs` with `@oai/artifact-tool` available, render the affected workbooks, and repackage. Keep before/after exercise comparisons on the same dataset.

### Validation and sharing

```sh
python3 reference-products/case2/tests/test_reference.py
python3 reference-products/case2/tests/evaluate_forecasts.py
node --check reference-products/case2/static/app.js
```

The local HTTP test opens a temporary loopback port. Live model tests are separate, explicitly invoked with `--run`, and consume API credits. Historical live-test claims belong to their original test date; do not label an offline rerun as a new API test.

Open the exported PDF and inspect changed slides. For syllabus edits, render the DOCX and inspect every page. Confirm local links, 83 slide pages, separate student/ground-truth archives, and a fresh extracted reference-app launch. Preserve `.env` and `local-state/` privately; the package builder uses an allowlist. Store logs, screenshots and inspection reports in the repository's ignored `build/ventures-package/`.

When paths or entry points change, update this README, the repository README and the relevant builders. Do not create a nested Git repository or retain duplicate dated delivery folders.
