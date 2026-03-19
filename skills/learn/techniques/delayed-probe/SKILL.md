---
name: delayed-probe
description: Quick surprise retention check. A 30-second mini-quiz to test if a concept is still in memory. Use for concepts with high stability that haven't been tested recently.
user-invocable: false
---

# Delayed Probe

A minimal, non-intrusive retention check. Takes 30 seconds max.

## How It Works

1. Pick a concept from the recommendations (one that the API suggests for `delayed_probe`)

2. Present ONE question, framed as a casual check:

> **Quick check** — You learned about [concept] [X days ago]. Your predicted recall is [Y%].
>
> [One clear question about the concept]

3. Accept the answer. Grade it.

4. Record via the probes endpoint:
```bash
curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  https://cognition-api.fly.dev/v1/probes/outcome \
  -d '{
    "probe_id": "probe-<uuid>",
    "concept_id": "<concept_id>",
    "horizon_days": <days_since_learned>,
    "predicted_recall": <predicted_R>,
    "result_correct": <true/false>,
    "result_score": <0.0-1.0>,
    "result_confidence": <user_confidence>
  }'
```

5. Give brief feedback:
   - Correct: "Still solid. Next check in [X] days."
   - Incorrect: "That's slipping. Want a quick review?" (offer to run spaced-retrieval)

## Probe Formats

Choose based on concept type:
- **free_recall**: "What do you remember about X?" (hardest, most diagnostic)
- **cued**: "X is used when ___" (medium)
- **mcq**: Multiple choice (easiest, good for quick checks)
- **teach_back**: "Explain X as if teaching a junior dev" (most revealing)

## Key Rules

- ONE question only. This is not a quiz.
- Keep it under 30 seconds total.
- Don't probe during focused work — check the screenpipe context first.
- If the user gets it wrong, don't drill — just note it and schedule a full review later.
