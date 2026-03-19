---
name: status
description: Show your current knowledge state — what you know, what's decaying, study stats
---

# Status — Your Knowledge Dashboard

## Steps

1. **Read token and fetch all state:**

```bash
TOKEN=$(cat ~/.cognition/token)

# Learner state (all concepts + recall probabilities)
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/learner-state?user_id=USER_ID"

# Recommendations (what needs attention)
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/recommendations?user_id=USER_ID&limit=10"

# Strategy signature (learner type)
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/strategy/signature?user_id=USER_ID"

# Calibration (confidence accuracy)
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/calibration/snapshot?user_id=USER_ID"

# Assessment report (mastery evidence)
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/assessment/report?user_id=USER_ID"
```

2. **Present as a dashboard:**

```
╔══════════════════════════════════════════════════╗
║              COGNITION STATUS                     ║
╠══════════════════════════════════════════════════╣
║                                                   ║
║  Concepts tracked: 47                             ║
║  Average recall:   74%                            ║
║  At risk (< 60%):  5 concepts                    ║
║  Strong (> 85%):   28 concepts                   ║
║                                                   ║
║  LEARNING STYLE: stable_retriever                ║
║  CALIBRATION: well-calibrated (ECE: 0.08)        ║
║                                                   ║
║  ── NEEDS REVIEW ──────────────────────────────  ║
║  ⚠ React useEffect cleanup     43%  1.5d left   ║
║  ⚠ SQL JOIN types              52%  3.0d left   ║
║  △ Git rebase workflow          61%  5.0d left   ║
║  △ Python decorators           64%  6.2d left   ║
║  △ CSS Grid vs Flexbox          67%  7.1d left   ║
║                                                   ║
║  ── STRONGEST CONCEPTS ────────────────────────  ║
║  ✓ Python list comprehensions  92%               ║
║  ✓ HTTP status codes           87%               ║
║  ✓ JavaScript promises         86%               ║
║                                                   ║
║  ── TODAY'S STUDY ─────────────────────────────  ║
║  Reviews completed: 8                             ║
║  Accuracy: 87%                                    ║
║  Concepts strengthened: 6                         ║
║                                                   ║
╚══════════════════════════════════════════════════╝
```

Fill in actual data from the API responses. Adjust the layout to fit the data.

If concepts are at risk, offer: "Want me to start a quick review? The most urgent concept is [X]."
