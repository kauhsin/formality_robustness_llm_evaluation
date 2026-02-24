# Week Retrospective

## Week 2 (20260216-20260222)
### What is achieved?
- Defined a **12-item evaluation rubric** and an **error taxonomy (v1)**.
- Built a three-stage pipeline for model inference and evaluation:
  - `run_api.py`: calls Gemini (2.5) to generate model responses and outputs structured JSON.
  - `score_outputs_stub.py`: evaluates model responses using the rubric (stub implementation).
  - `pair_stub.py`: aggregates and pairs evaluation results by intent for controlled comparison.
- Wired the pipeline to a real LLM API (Gemini) and successfully ran end-to-end inference on a small head dataset (4 paired samples).
- Verified that the end-to-end pipeline (dataset -> API -> scoring -> pairing) is functional.

### What were the challenges?
- Free-tier quota and rate limits on the Gemini API interrupted batch runs.
- Per-row API calls are not scalable due to latency and rate limits; batching or throttling will be needed for larger runs.

### Open issues / risks
- Free-tier quotas are too restrictive for running the full dataset; need a sustainable inference strategy (throttling, batching, or alternative API/provider).