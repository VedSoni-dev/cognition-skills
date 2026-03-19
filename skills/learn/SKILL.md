---
name: learn
description: Generate and deliver a learning exercise based on what the user is forgetting. Orchestrates different learning techniques.
---

# Learn — The Intervention Engine

This is the master learning skill. It decides which technique to use and executes it.

## Steps

1. **Get the data** — call predict endpoints (recommendations, learner state, strategy signature, calibration)

2. **Decide the technique** based on the API response:

| Condition | Technique | Why |
|-----------|-----------|-----|
| Lapses > 0 for this concept | **Spaced Retrieval** | They've forgotten before — need active recall |
| Recommendation action = "quiz" | **Spaced Retrieval** | API recommends quiz |
| Strategy = "overconfident" | **Calibration Check** | They think they know it but don't |
| Strategy = "cram_dependent" | **Interleaving** | Break the cramming pattern |
| Multiple related concepts decaying | **Interleaving** | Practice related concepts together |
| Concept has high stability but hasn't been tested | **Delayed Probe** | Quick surprise check |
| Recommendation action = "review" | **Replay Consolidation** | Multi-phase memory replay |
| User asks to explain something | **Teach Back** | Explain it to prove mastery |

3. **Check the stability budget** before intervening:
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/stability/budget?user_id=USER_ID"
```
If the budget says the intervention would destabilize learning, defer or soften the exercise.

4. **Execute the technique** — load the specific technique skill and follow its instructions.

5. **Record results** via the reflect flow — POST quiz_answer or delayed_probe events back to the API.

## Delivery Modes

**Terminal mode** (default): Present exercises as interactive markdown. Ask questions, wait for answers, give feedback.

**Rich UI mode**: When the exercise benefits from visual interaction (knowledge maps, multi-question quizzes), generate an HTML file using the scripts in `scripts/` and open it in the browser:
```bash
python ${CLAUDE_SKILL_DIR}/../scripts/quiz.py --output /tmp/cognition-quiz.html
# then open it
```

## After the Exercise

Always show:
- How many questions right/wrong
- How stability changed for each concept
- When the next review is predicted
- Encouragement based on progress
