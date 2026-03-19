---
name: interleaving
description: Mix related concepts together in practice. Use when the interleaving plan suggests concept pairs or when the user's strategy is "cram_dependent".
user-invocable: false
---

# Interleaved Practice

Instead of drilling one concept at a time, alternate between related concepts. This builds discrimination ability and reduces interference.

## Steps

1. **Get the interleaving plan** from the API:
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/interleaving/plan?user_id=USER_ID"
```

This returns concept pairs with:
- `concept_a`, `concept_b` — the pair
- `spectral_distance` — how related they are
- `transfer_potential` — likelihood of positive transfer
- `interference_risk` — likelihood of confusion
- `recommended_mode` — `compare`, `contrast`, or `alternate`

2. **Generate interleaved questions:**
   - Q1: Concept A question
   - Q2: Concept B question
   - Q3: "How does [A] differ from [B]?" (discrimination question)
   - Q4: Concept A again (context switch cost = learning)
   - Q5: "When would you use [A] vs [B]?" (transfer question)

3. **The key principle:** The difficulty is in the switching, not the questions. Questions can be medium difficulty — the interleaving IS the challenge.

4. **Example flow:**

> **Interleaved Practice: SQL JOINs × Array Methods**
>
> Q1: What does a LEFT JOIN return when there's no match in the right table?
> Q2: What does Array.filter() return when no elements match the predicate?
> Q3: Both LEFT JOIN and filter() handle "no match" cases. How do their approaches differ?
> Q4: Write a SQL query that returns all users and their orders (including users with no orders).
> Q5: When would you use a subquery vs a JOIN? When would you use filter() vs reduce()?

5. **Record results** — tag each question with both concept IDs in the concept_tagging.
