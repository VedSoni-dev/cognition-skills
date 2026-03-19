---
name: spaced-retrieval
description: Active recall quiz at optimal spacing intervals. The core spaced repetition technique. Use when the API recommends "quiz" or the concept has lapses > 0.
user-invocable: false
---

# Spaced Retrieval Practice

The most effective learning technique. Force the user to recall information without hints.

## How to Generate Questions

1. Use the concept label and any context from the learner state
2. Generate 2-3 questions per concept, varying in format:
   - **Multiple choice** (4 options, 1 correct) — for recognition
   - **Short answer** — for recall
   - **True/false with explanation** — for understanding

3. Match difficulty to the user's ZPD band from the API:
   - `below`: easier questions, more scaffolding
   - `inside`: challenging but achievable
   - `above`: stretch questions with hints available

## Question Flow

For each question:

1. Present clearly with context:
   > **Q1/3** — React Hooks (retrievability: 43%, last reviewed: 3 days ago)
   >
   > What happens when you return a function from useEffect?
   >
   > a) It runs immediately on mount
   > b) It runs when the component unmounts or before the effect re-runs
   > c) It prevents the effect from running again
   > d) It caches the effect's dependencies

2. Wait for the user's answer

3. Grade:
   - Correct: score 1.0, is_correct true
   - Partially correct (right idea, wrong details): score 0.5, is_correct false
   - Incorrect: score 0.0, is_correct false

4. Give feedback:
   - Correct: brief confirmation + one reinforcing fact
   - Incorrect: explain why, connect to what they do know, no shaming

5. Record via reflect flow with:
   - `question_type`: multiple_choice / short_answer / true_false
   - `difficulty`: easy / medium / hard / zpd
   - `is_correct`: bool
   - `evaluation_score`: 0.0-1.0
   - `latency_ms`: time from question shown to answer
   - `confidence_self_report`: ask "How confident were you?" (1-5 scale, map to 0-1)

## Spacing Logic

The API handles spacing via the Weibull decay model. After recording results, the API updates stability and difficulty. The next review time is computed server-side. Just report results accurately.
