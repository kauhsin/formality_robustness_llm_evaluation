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