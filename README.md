## Dataset Overview

This dataset consists of controlled pairs of user queries that express the same underlying intent in different linguistic registers. The goal is to analyze how language variation impacts LLM understanding and response quality.

---

## Dataset Schema

Each data point represents a single user query.

**Fields:**
- `id` (string): Unique identifier for the sample.
- `intent_id` (string): Identifier shared by variants of the same intent.
- `register` (enum): Linguistic register of the input.  
  - `formal`  
  - `informal`
- `phenomena` (list of enum): High-level linguistic phenomena present in the input. Multiple labels may co-occur.
- `query` (string): The user input text.

---

## Example

```json
{
  "id": "001_ns",
  "intent_id": "001",
  "register": "informal",
  "phenomena": ["abbreviation"],
  "query": "What’s a good gift for a 5yo kid?"
}
```


## Linguistic Phenomena Labels

A lightweight, product-oriented set of labels is used to characterize language variation in user inputs.

* **abbreviation**
Shortened forms commonly used in informal contexts (e.g., "5yo", "u", "pls").
  *Product relevance:* May affect entity recognition and intent understanding.

* **typo** Spelling errors or character-level noise (e.g., "definately", "recieve").
  *Product relevance:* May degrade keyword matching and retrieval, and introduce ambiguity in user intent.

* **informal_lexicon** Informal or colloquial word choices (e.g., "kid", "kinda", "gonna").
  *Product relevance:* May influence register and affect intent classification or tone adaptation in responses.
  
* **dialect_word** Regionally specific or dialectal vocabulary. 
  *Product relevance:* May be underrepresented in training data and lead to misunderstandings for certain user populations.
  
* **noncanonical_syntax** Non-standard or conversational syntactic structures (e.g., "how get a better sleep?")
  * Product relevance:* May affect parsing and intent extraction in user queries.
--- 

## Labeling Notes 

* Multiple phenomena can co-occur in a single input (e.g., ["abbreviation", "informal_lexicon"]).

* The label set is designed to be lightweight and product-oriented rather than a fine-grained linguistic taxonomy.

* Minor surface variations (e.g., capitalization) are not annotated as separate phenomena in v1.

## Need to add later

The initial dataset uses synthetic informal variants to bootstrap the evaluation pipeline.

In later phases, I plan to incorporate naturally occurring user queries to improve ecological validity and stress-test robustness under real-world noise.

--- 

We treat query-style forms like “how to reset router” as in-distribution user inputs, since they are very common in real-world training data.

Our robustness analysis focuses on more disruptive variants such as typos, abbreviations, dialectal words, and informal lexicon that are more likely to cause distribution shift.

---