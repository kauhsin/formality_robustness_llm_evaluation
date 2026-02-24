# Dialect-word Pilot Dataset COnstruction Notes (v0)

I narrowed the broader formal vs informal robustness question into a more testable subproblem: **dialect lexical variation** and intent recognition.

Here are the points I found helpful in creating the toy dataset:

- Prioritized lexical variants that can cause **real semantic misinterpretation**, not just surface wording differences.
    - Good example: rubber (UK eraser vs another common meaning), mad (very vs angry).
    - Counterexample: kid vs child (same intent, mostly wording style).

- Avoided examples where both interpretations could still produce a plausible answer, because they are hard to score reliably. Chose samples where a wrong interpretation would leave clear evidence in the response
    - Example to avoid: biscuit/cookie in a café context, since both can still lead to a generic food answer.
    - Better example: fit/outfit, where a wrong reading can clearly change the advice.

- Treated context strength as a controlled variable, since too little context is noisy and too much context lets the model recover too easily
    - Weak-context example: “I forgot my rubber. Can I borrow one?”
    - Strong-context example: “Can I use a rubber to erase pencil marks?” (much easier to infer correctly).

- Avoided overly strong disambiguation cues when the goal is to test lexical mapping rather than context-based recovery
    - Too-strong cue to avoid (for lexical tests): “erase pencil marks” with rubber.
    - Better lexical test: “Can I borrow a rubber at school” with only light context.

- Avoided location-dependent prompts like “nearby” or “here” to prevent confounds from missing real-world context, as LLM has no clue of the physical location of the user in the project.  
    - Confounded example: “Where can I get chips nearby?” (may trigger location clarification).
    - Better example: “Should I reheat chips in the oven or microwave?” (tests lexical understanding directly).

- Kept formal and informal pairs semantically aligned, changing only the target lexical form to preserve a clean comparison
    - Good pair: “I like your outfit” vs “I like your fit” in the same compliment intent.
    - Counterexample: changing both the lexical item and the task (for example, complimenting outfit in one version but asking for dating advice in the other).

- Reduced repeated patterns and aimed for more domain variety to improve coverage
    - Better coverage example: mix eraser/rubber (school), mad cold (home/weather), fit/outfit (social).
    - Counterexample: too many food-only pairs like fries/chips, cookie/biscuit, etc.

And besides all abpve, I should always design examples with the rubric in mind, so errors would be observable on intent, entity or slot handling, robustness, and response quality

# Dialect-word Pilot Retro/Analysis Notes (v0)

**Date:** 2026-02-24  
**Scope:** intent pairs 061–064 (dialect-word / informal lexical variants)  
**Model:** Gemini (API run, manual review + manual rubric scoring)

---

## What I tested in this mini-pilot

I ran a small dialect-word subset (intent pairs 061–064) and manually scored the outputs using the current rubric.

Main question for this round:

- If the query only changes a dialect/informal lexical item, does the model still capture the same user intent?
- If yes, what else changes (verbosity, relevance, style, extra explanation, task focus)?

This was a behavior check, not a benchmark result.

---

## High-level result (main takeaway)

The model handled the dialect-word variants better than expected.

In all current examples, it correctly recovered the intended meaning of the lexical item when there was at least a small amount of local context.

Examples:
- `rubber` + `at school` -> correctly interpreted as **eraser**
- `chips` + reheating context -> correctly interpreted as **fries / hot potato side**
- `mad cold` -> correctly interpreted as **very cold**
- `fit` -> correctly interpreted as **outfit / look / style**

So in this toy set, the main issue is not intent failure. The model usually gets the meaning right.

This means the next phase should not only test "did it understand the word," but also how the dialect form changes response behavior.

---

## What kind of differences I did see

Even when intent recognition stayed strong, dialect-word variants sometimes changed **how** the model responded.

Most visible differences:
- extra lexical explanation (not requested by user)
- verbosity
- task boundary discipline (stays on task vs expands task)

So the effect is often not "wrong vs right," but:
- task alignment
- response calibration
- over-explaining

This is still useful for conversational evaluation.

---

## Pattern 1: Correct answer + extra lexical note (061 "rubber")

### What happened

For the informal query (`I forgot my rubber. Can I borrow one at school?`), the model:

- correctly understood `rubber` = eraser
- correctly answered the actual user question
- then added a regional lexical note ("rubber" in North America)

### Why this matters

The answer is still correct, but the added lexical note was not part of the user’s task.

This makes the response feel less task-focused and more lecture-like than necessary.

### How I scored it

I kept high scores for intent / slot / robustness items.

I deducted on:
- **R7 (irrelevant/inappropriate content)** because the lexical note was not requested
- **R10 (conciseness)** because the extra section made the response longer than needed

### Working hypothesis

The model may be "playing it safe" because `rubber` has a socially sensitive alternate meaning in some regions.

Even though the school context is enough to disambiguate, it still proactively explains the ambiguity.

---

## Pattern 2: Correct answer + more task-focused response (064 "fit")

### What happened

For the informal query (`How can I politely tell someone I like their fit?`), the model:

- correctly interpreted `fit` as outfit/look
- gave practical phrasing suggestions
- stayed relatively direct and useful

Compared with the formal `outfit` version, the informal one actually felt more direct and less padded.

### Why this matters

Informal/dialect wording is not always a "harder" version that lowers response quality.

In some cases, the informal form may produce a response that is:
- more natural
- more direct
- more useful for the user’s actual task

### Important nuance

`fit` could also have triggered extra caution or lexical explanation, but it did not.

So the model’s tendency to add lexical notes is not consistent across all ambiguous/sensitive words.

---

## Cases with little meaningful formal–informal difference (062 "chips", 063 "mad cold")

### 062 (`fries` vs `chips`)

The model correctly handled the lexical mapping and gave the same core recommendation (oven > microwave).

The main issue in both versions was over-answering (full air fryer / extra method sections), not lexical misunderstanding.

So in this pair:
- the dialect word itself did not cause an intent failure
- the bigger issue was task expansion

### 063 (`very cold` vs `mad cold`)

The model handled `mad cold` correctly and gave a very similar practical response to the formal version.

This suggests some dialect intensifiers are already very easy for the model and may not be strong test cases unless the task is tighter or the context is more ambiguous.

---

## Rubric calibration notes from this round (important)

This pilot was helpful for calibrating **R7 (irrelevant content)** and **R10 (conciseness)**.

I cannot score these based on length alone. I need to judge whether extra content is:

### A) Task-adjacent helpful elaboration (often acceptable)

Example:
- `It is very cold in my apartment. Should I turn up the heat?`
- Extra steps (thermostat, vents, landlord) are still aligned with the user’s likely practical goal

### B) Task-expanding content (should be penalized)

Example:
- `Should I reheat fries/chips in the oven or in the microwave?`
- Adding full sections for air fryer and other methods expands the task beyond the user’s explicit choice

This distinction should stay part of the scoring logic.

---

## Current interpretation of dialect-word effect (v0)

At this stage, my working interpretation is:

- The model is generally strong at dialect-word meaning recovery when there is minimal context.
- The bigger differences show up in response behavior, especially:
  - extra lexical commentary
  - verbosity
  - task-boundary discipline
- The strongest visible difference so far appears when the word has a potentially sensitive or socially loaded alternate meaning (example: `rubber`)
- In less sensitive cases (`chips`, `mad cold`), formal and informal outputs are often very similar
- In some cases (`fit`), the informal version may even produce a more efficient response than the formal version

So, in this pilot, dialect variation affects **how the model answers** more than **whether it understands the question**.

---

## What I still do not know yet

Open questions for next rounds:

1. Is extra lexical explanation actually tied to sensitivity/risk?
   - `rubber` suggests yes
   - `fit` suggests not always
   - need more examples

2. How stable is this behavior across repeated runs / other models?
   - current pilot is too small to tell

3. Are current examples hard enough?
   - probably not yet
   - many are recoverable with easy context

4. Will tighter task types show stronger differences?
   - transactional / support / instruction-following tasks may expose clearer downstream errors

---

## What this changes in next-step dataset design

Next examples should still use dialect-word pairs, but prioritize cases where:

- the alternate interpretation is plausible
- the wrong interpretation would cause clearly different response content
- context is present but not too strong
- scoring is clear on task alignment and relevance

I also want to explicitly track not only "got the meaning right," but whether the model:

- adds unrequested lexical commentary
- becomes overly cautious
- becomes more verbose
- drifts outside the user’s task boundary

This feels more realistic for industry-style evaluation than intent accuracy alone.

---

## Practical conclusion for this pilot

This was a productive pilot even without many outright failures.

What I got:

- evidence that many dialect-word variants are robustly handled
- clearer understanding of where differences actually show up
- better scoring calibration (especially R7 and R10)
- better criteria for designing stronger next-round examples

Next step:
- run another small batch with harder lexical ambiguity and stronger downstream consequences
- keep the same rubric
- continue collecting qualitative behavior notes, not just score totals

---

## Reusable one-paragraph summary (for README / report draft)

In a small dialect-word pilot, the model consistently recovered intended meanings from informal/dialect lexical variants given minimal context. The main differences were not intent failures but response behavior differences, especially extra lexical explanation and verbosity in some cases. This suggests the next phase should test dialect robustness not only as semantic understanding, but also as task alignment and response calibration.