---
name: predict
description: Check what knowledge is decaying and what needs review. Shows recommendations from the Cognition API.
---

# Predict — What Are You Forgetting?

## Steps

1. **Read the auth token:**
```bash
TOKEN=$(cat ~/.cognition/token)
```

2. **Get recommendations:**
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/recommendations?user_id=USER_ID&limit=10"
```

3. **Get learner state:**
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/learner-state?user_id=USER_ID"
```

4. **Get strategy signature** (what kind of learner they are):
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/strategy/signature?user_id=USER_ID"
```

5. **Get calibration snapshot** (are they over/under-confident?):
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/calibration/snapshot?user_id=USER_ID"
```

## How to Present

Show the user a clear summary:

```
🧠 Knowledge State

📉 Decaying (needs review soon):
  • React useEffect cleanup — 43% recall, critical in 1.5 days
  • SQL JOIN types — 52% recall, critical in 3 days
  • Git rebase workflow — 61% recall, critical in 5 days

📊 Strong (no action needed):
  • Python list comprehensions — 92% recall
  • HTTP status codes — 87% recall

🎯 Your learning style: stable_retriever
📐 Calibration: well-calibrated (ECE: 0.08)

Recommended: Quiz on useEffect cleanup (highest priority)
```

If there are urgent recommendations, offer to start a learning exercise immediately by invoking the learn skill.
