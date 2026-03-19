---
name: teach-back
description: User explains a concept back to prove mastery. The most demanding and most effective technique. Use when the user explicitly asks to review or when testing deep understanding.
user-invocable: false
---

# Teach-Back

The user teaches the concept to you (the AI). This is the highest-fidelity test of understanding.

## Flow

1. **Prompt:**
> Teach me about [concept] as if I'm a junior developer who's never seen it before.
> I'll ask follow-up questions to test your understanding.

2. **Evaluate their explanation** for:
   - **Accuracy** — are the facts correct?
   - **Completeness** — did they cover key aspects?
   - **Depth** — do they understand WHY, not just WHAT?
   - **Examples** — can they give concrete examples?
   - **Connections** — do they relate it to other concepts?

3. **Ask follow-up questions** that probe gaps:
   - "What happens if [edge case]?"
   - "How is this different from [related concept]?"
   - "Can you give me a real-world example?"
   - "Why does it work that way instead of [alternative]?"

4. **Grade on a 4-point scale:**
   - 4 (mastery): Accurate, complete, with examples and connections
   - 3 (proficient): Mostly accurate, covers main points
   - 2 (developing): Some correct ideas but significant gaps
   - 1 (novice): Mostly incorrect or "I don't remember"

5. **Give feedback:**
   - What they got right (reinforce)
   - What they missed (fill the gap)
   - One thing to focus on (actionable)

6. **Record** as a quiz_answer event with:
   - `question_type`: "short_answer"
   - `evaluation_score`: mapped from the 4-point scale (4→1.0, 3→0.75, 2→0.4, 1→0.15)
   - `is_correct`: true if grade >= 3

## When to Use

- User says "I think I know this well" — test it
- Concept has high stability but low review count — verify it's real mastery
- Strategy signature is "overconfident" — reality check
- Before an exam or presentation — practice explaining
