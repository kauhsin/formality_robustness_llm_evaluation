# Manual scoring inputs (v0)

CSV schema: intent_id, register, rubric_id, rubric_number, score
CSV location: outputs/manual_scores/

Current files:
- outputs/manual_scores/initial_pilot_v0.csv
- outputs/manual_scores/dialect_word_pilot_v0.csv

Scoring rules:
- R1–R7: score ∈ {0, 2}
- R8–R10: score ∈ {0, 1}
- max_total_score per response = 17

Grouping key for totals: (intent_id, register)
Pairing key for deltas: intent_id (formal vs informal)

## score_outputs_v0 notes

Script:
- `src/cli/score_outputs_v0.py`

Current input:
- Manual scoring CSV only
- Default input path: `outputs/manual_scores/dialect_word_pilot_v0.csv`

Current outputs:
- Response-level score summary JSON: `outputs/score_summary_dialect_word_pilot_v0.json`
- Pair-level score summary JSON: `outputs/pairing_dialect_word_pilot_v0.json`

Current assumptions:
- Max total score per response = 17
- Rubric items = 10
- Scoring style = binary
- Input CSV schema: `intent_id, register, rubric_id, rubric_number, score`

Current behavior:
- Reads manual scoring CSV
- Filters to valid rows based on register, rubric range, and allowed score values
- Aggregates response-level total scores by `(intent_id, register)`
- Aggregates pair-level formal vs informal deltas by `intent_id`

Next step:
- Reuse the same flow for other slices (for example: `initial_pilot_v0`, multi-slot, typo, noncanonical syntax)
- Optionally make output naming auto-derived from input CSV name