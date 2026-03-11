# Pipeline v0 (quick scope)

**Goal:** one CLI entry to run `run_api → pretty_print → (optional) score → (optional) compare`, with safe defaults.

**Inputs:**
- `--dataset_jsonl` (required)
- `--scores_csv` (optional; if provided, run scoring + pairing)
- `--skip_api` / `--force` (optional)

**Outputs (default locations):**
- `outputs/after_api/`: `run_api_*.json`, `score_summary_*.json`, `pairing_*.json`, `cross_slice_metrics_v0.json` (optional)
- `outputs/human_readable/`: pretty output `.txt` / `.md`

**QA (minimal):**
- If `--scores_csv` is given: each `(intent_id, register)` must have **10 rows** (R1–R10), else error.
- Pairing requires both `formal` and `informal` per intent_id, else error.