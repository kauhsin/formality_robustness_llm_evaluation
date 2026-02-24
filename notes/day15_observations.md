# Day 15 Observations

## Observation 1
Across the currently evaluated rubric items, there is no clear performance difference between formal and informal variants in this pilot sample.

### Evidence
For both intent pairs (001 and 002), the formal and informal responses appear similarly strong on intent understanding, task alignment, safety, and overall readability. No obvious degradation is observed in the informal variants.

### Implication
At least for these two examples, the model appears robust to light register variation.

---

## Observation 2
The formal and informal prompts produce highly similar responses in both content and organization, with only minor differences in details.

### Evidence
For the gift recommendation pair (intent 001), both responses use a categorized list structure and cover similar gift types. The differences are mostly in specific examples and category breakdown details rather than in core task performance.
For the microwave safety pair (intent 002), both responses deliver the same main conclusion, similar safety reasoning, and similar exception handling structure.

### Implication
The model appears to normalize light informal phrasing into a similar response pattern, preserving content structure across register variants.

---

## Observation 3
No clear advantage is observed for the formal variant in this pilot. In at least one case, the formal response is more verbose, while the informal response is comparably informative and not necessarily more wordy.

### Evidence
In the current pilot sample, one formal response (001_formal) appears overly long relative to the user query, while the corresponding informal response (001_informal) remains similarly informative with slightly more compact organization.

### Implication
Differences between formal and informal variants may show up more in verbosity or response style than in correctness.

---

## Observation 4
The current pilot sample is too small and too easy to serve as a reliable robustness test.

### Evidence
Only two intent pairs were evaluated. In addition, the informal variants are relatively mild (e.g., `5yo`, `zap`) and remain easy to interpret.

### Implication
This pilot validates the pipeline and rubric usability, but a stronger test set is needed to meaningfully evaluate robustness to non-standard language variation.

---

## Next step
Add more intent pairs with harder informal variants (e.g., typos, compressed phrasing, slot-heavy queries, colloquial wording) and run another targeted pilot evaluation.

Next step: Add harder informal variants (typos, compressed phrasing, slot-heavy queries) to increase the chance of observable robustness differences.