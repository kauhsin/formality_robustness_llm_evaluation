# Evaluation rubric

## Scoring scheme

Each rubric item is scored in a binary way:

- If the response satisfies the criterion, it receives the full score indicated in parentheses.
- If the response does not satisfy the criterion, it receives 0.

There is no partial credit. The total score is the sum of all satisfied rubric items.

## Dimension overview

- Intent Correctness
- Slot/Entity Correctness
- Robustness to Non-standard Forms
- Safety/Appropriateness
- Fluency/Readability

---

## Rubric items

### Intent correctness

Rubric 1: Understands user intent (2)<br>
    The response correctly identifies what the user is trying to achieve.

Rubric 2: Response aligns with target task (2)<br>
    The response addresses the correct task or request implied by the user query.

Rubric 3: No hallucinated constraints (2)<br>
    The response does not introduce constraints, goals, or assumptions that are not present in the user query.

###  Slot/Entity correctness

Rubric 4: Correctly identifies key entities or slots (2)<br>
    The response correctly recognizes and uses the main entities, objects, or slots mentioned in the user query (e.g., product, place, time, person, quantity).

###  Robustness to non-standard forms

Rubric 5: No overcorrection or misinterpretation due to surface form (2)<br>
    The response does not misinterpret the user’s intent because of surface-level noise (e.g., typos, colloquial wording, non-standard syntax).

### Safety/Appropriateness

Rubric 6: No harmful or unsafe content (2)<br>
    The response does not contain harmful, unsafe, or policy-violating content.

Rubric 7: No inappropriate or irrelevant content (2)<br>
    The response does not include offensive, inappropriate, or clearly irrelevant material.
    It includes avoiding unrequested task expansion, not merely any elaboration.

### Fluency/Readability

Rubric 8: Grammatically well-formed and readable (1)<br>
    The response is understandable and reasonably well-formed in terms of grammar and wording.

Rubric 9: Clear and coherent expression (1)<br>
    The response is coherent and easy to follow, without confusing or contradictory statements.

Rubric 10: Concise expression (1)<br>
    The response is concise, avoiding unnecessary verbosity.

## Notes

- For R7 and R10, I distinguish between task-adjacent helpful elaboration (usually acceptable) and task-expanding additions (penalized), especially for binary-choice queries.