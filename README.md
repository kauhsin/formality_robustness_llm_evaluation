# LLM Variant Robustness Evaluation
## Problem

Large language models often perform well on clean, standard inputs, but their behavior under non-standard, real-world language variation (e.g., typos, abbreviations, colloquial or dialectal forms) is less well understood.
This project evaluates how such linguistic variation affects intent understanding and downstream response quality in realistic user queries.

The goal is to build a lightweight, reproducible pipeline for probing LLM robustness to non-standard language variants under controlled comparisons.

---

## What’s implemented (v0)

The current version focuses on dataset health checks and controlled evaluation setup:

- Intent-matched formal–informal query pairs to isolate the effect of language variation
- Lightweight linguistic phenomena labels (e.g., typo, abbreviation, informal_lexicon)
- Dataset composition statistics (by register and phenomenon)
- Automatic pairing validation to ensure each intent has both formal and informal variants (`bad_pairing_analysis`)

---

## Method

The evaluation pipeline is built around intent-matched formal–informal pairs and simple, transparent analysis steps:

- `Controlled pairing`: Each intent is represented by a formal and an informal variant to isolate the effect of language variation.
- `Variant labeling`: Each input is annotated with high-level linguistic phenomena (e.g., typo, abbreviation, dialect_word).
- `Statistics`: Aggregate counts by register and phenomenon to inspect dataset composition.
- `Pairing check`: Validate that each intent_id has both formal and informal variants for controlled analysis.
- `(Planned)` Error analysis and rubric-based evaluation of LLM outputs in later phases.

This design supports systematic comparison between standard and non-standard language inputs while remaining lightweight and easy to extend.


Evaluation rubrics and error taxonomy are documented under `docs/`.

---

## Evaluation

Model-output evaluation includes:

- Rubric-based grading of model responses for intent understanding and response quality (see `docs/rubric_v1.md`)
- Error taxonomy to categorize common failure modes (see `docs/error_taxonomy_v1.md`)
- Aggregate metrics and slice analysis by register and linguistic phenomenon

This structure allows systematic comparison between standard and non-standard inputs while keeping the evaluation transparent and reproducible.

---

## How to run

Generate summary reports from a JSONL dataset (*Bash code*):

```bash
python src/main.py data/dataset_v0.jsonl --out outputs/summary_v0.json
```
All generated reports are saved under `outputs/`.

---

## Outputs

All generated reports are saved under `outputs/`.

The summary report includes:

- Dataset composition statistics (`by_register`, `by_phenomena`)
- Pairing validation results (`bad_pairing_analysis`), indicating intents with missing formal or informal variants

These reports support controlled robustness analysis and dataset quality inspection.

### Pairing check

The dataset is organized around intent-matched formal–informal pairs.<br>
For each intent_id, the pipeline checks whether both variants are present to ensure valid controlled comparisons.

Intents with missing variants are reported under bad_pairing_analysis in the output JSON.

---

## Dataset
### Overview

This dataset contains controlled pairs of user queries that express the same intent in different linguistic registers (formal vs. informal).

The goal is to evaluate how non-standard language variation affects LLM intent understanding and response quality in realistic user inputs.

---

### Dataset schema

Each data point represents a single user query.

**Fields:**

- `id` (string): Unique identifier for the sample.
- `intent_id` (string): Identifier shared by variants of the same intent.
- `register` (enum): Linguistic register of the input.
  - `formal`
  -  `informal`
- `phenomena` (list of enum): High-level linguistic phenomena present in the input. Multiple labels may co-occur.
- `query` (string): The user input text.

---

### Example

*json*
```json
{
  "id": "001_ns",
  "intent_id": "001",
  "register": "informal",
  "phenomena": ["abbreviation"],
  "query": "What’s a good gift for a 5yo kid?"
}
```
---

### Linguistic phenomena labels

The dataset uses a lightweight, product-oriented label set to characterize language variation commonly observed in real user queries.

* **abbreviation**<br>
  Shortened forms commonly used in informal contexts (e.g., "5yo", "u", "pls").<br>
  *Product relevance:* May affect entity recognition and intent understanding.

* **typo**<br>
  Spelling errors or character-level noise (e.g., "definately", "recieve").<br>
  *Product relevance:* May degrade keyword matching and retrieval, and introduce ambiguity in user intent.

* **informal_lexicon**<br>
  Informal or colloquial word choices (e.g., "kid", "kinda", "gonna").<br>
  *Product relevance:* May influence register and affect intent classification or tone adaptation in responses.
  
* **dialect_word**<br>
  Regionally specific or dialectal vocabulary.<br>
  *Product relevance:* May be underrepresented in training data and lead to misunderstandings for certain user populations.
  
* **noncanonical_syntax**<br>
  Non-standard or conversational syntactic structures (e.g., "how get a better sleep?")<br>
  *Product relevance:* May affect parsing and intent extraction in user queries.
--- 

### Labeling notes 

* Multiple phenomena may co-occur in a single input (e.g., ["abbreviation", "informal_lexicon"]).

* The label set is designed to be lightweight and product-oriented rather than a fine-grained linguistic taxonomy.

* Minor surface variations (e.g., capitalization) are not annotated as separate phenomena in v1.

---

### Dataset scope and roadmap

The current dataset uses controlled synthetic informal variants to bootstrap the evaluation pipeline.<br>
Future iterations will incorporate naturally occurring user queries to improve ecological validity and stress-test robustness under real-world noise.

Query-style inputs such as “how to reset router” are treated as in-distribution user queries.
The robustness analysis focuses on more disruptive variants (typos, abbreviations, dialectal words, informal lexicon) that are more likely to introduce distribution shift.

---

## Repo layout

- `data/` # JSONL datasets
- `docs/` # Dataset description, rubrics, and error taxonomy
- `src/` # Pipeline scripts
- `outputs/` # Generated summary reports

---

## Roadmap(v1/v2)

**v1 (next)**
- Run inference on selected LLMs for formal vs. informal pairs
- Apply rubric-based scoring to model outputs
- Aggregate metrics and slice analysis by phenomenon and register

**v2 (later)**
- Incorporate naturally occurring user queries
- Add human-in-the-loop adjudication for ambiguous cases
- Analyze model consistency and failure patterns across variants