# Replenishment case data

The student package contains only historical weekly sales, current stock, planned inbound and the initial calculation contract. The instructor package adds hidden business context, staged expected decisions and an independently simulated next week.

- [Runnable instructor reference](../../reference-products/case2/README.md): dashboard + chatbot, staged context, [walkthrough](../../reference-products/case2/WALKTHROUGH.md) and [test report](../../reference-products/case2/TEST_REPORT.md).
- [Student data](student-data/README.md)
- [Student ZIP](student-data.zip)
- [Instructor ground truth](ground-truth/README.md)
- [Ground-truth ZIP](ground-truth.zip)

Use the same frozen snapshot for classroom comparisons: **16 November 2026**. Historical sales end on **15 November**; the hidden actual week is **16-22 November**. Every value is synthetic.

## Rebuild

Run these commands from the course root.

1. Run `python3 assets/data-generation/generate_data.py` to recreate raw inputs and truth from the fixed seed.
2. Run `python3 assets/data-generation/verify_data.py` to verify joins, time periods, anomalies, stage behaviour, inventory reconciliation and hand-calculated answers.
3. With the bundled artifact-tool dependencies available through `NODE_PATH`, run `node assets/data-generation/build_workbooks.mjs` to create the two Excel reading copies. Set `DATA_PREVIEW_DIR` to an ignored build directory for visual QA images.
4. Run `python3 assets/data-generation/package_data.py` to rebuild the student and instructor distribution ZIPs.

Do not distribute the ground-truth ZIP or the data-generation source before learners complete the initial exercise. Keep the initial student package unchanged when revealing later context so before-and-after results remain comparable.
