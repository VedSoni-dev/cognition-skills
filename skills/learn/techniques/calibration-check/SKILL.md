---
name: calibration-check
description: Test if the user's confidence matches their actual knowledge. Use when calibration ECE is high or strategy is "overconfident".
user-invocable: false
---

# Calibration Check

Detect and correct the gap between what the user THINKS they know and what they ACTUALLY know.

## Flow

1. **Get calibration data:**
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/calibration/snapshot?user_id=USER_ID"
```

2. **Pick 5 concepts** — mix of high and low retrievability

3. **For each concept, ask TWO things:**

> **Concept: [X]**
>
> First: How confident are you that you could explain [X] right now? (1-5)
>
> Now: [actual question about X]

4. **Compare predicted vs actual:**

After all 5:
```
Calibration Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Concept              Confidence  Actual  Gap
useEffect cleanup    5/5         ✗       OVERCONFIDENT
SQL JOINs            2/5         ✓       UNDERCONFIDENT
Git rebase           4/5         ✓       Calibrated
Python decorators    3/5         ✗       Calibrated
CSS Grid             4/5         ✗       OVERCONFIDENT

Overall: You tend to overestimate your recall.
ECE: 0.32 (needs work — below 0.15 is well-calibrated)
```

5. **Coaching:**
   - Overconfident: "You rated [X] at 5/5 but couldn't answer. This is the most dangerous state — you won't review what you think you already know. Try rating yourself 1 point lower than your gut says."
   - Underconfident: "You rated [X] at 2/5 but got it right! You know more than you think. Trust your recall."
   - Well-calibrated: "Your confidence matches your knowledge. Keep it up."

6. **Record** all results as quiz_answer events with confidence_self_report values.

## Why This Matters

Overconfidence is the #1 enemy of learning. If you think you know something, you won't review it. If you don't review it, it decays. The calibration check breaks this cycle.
