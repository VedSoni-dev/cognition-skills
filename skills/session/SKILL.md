---
name: session
description: Run a full study session — observe, predict, and practice in one flow
disable-model-invocation: true
---

# Study Session

Run a complete learning loop.

## Flow

### 0. Pre-check
Ensure Screenpipe is running. If not, start it:
```bash
curl -s http://localhost:3030/health 2>/dev/null || (npx screenpipe@latest record > /dev/null 2>&1 & sleep 5)
```

### 1. Observe
Use the screenpipe MCP tools to check what the user has been doing in the last hour. Summarize the learning-relevant content.

### 2. Ingest
For each learning-relevant observation, POST a `screen_capture` event to the Cognition API:

```bash
TOKEN=$(cat ~/.cognition/token)
curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  https://cognition-api.fly.dev/v1/events \
  -d '{ "event": { ... screen_capture event ... } }'
```

Use the event schema from llms.txt. Generate proper UUIDs for event_id and idempotency_key.

### 3. Predict
Fetch recommendations and learner state. Show the user what's decaying.

### 4. Plan
Get the world model plan for optimal intervention:
```bash
curl -s -X POST -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/world-model/plan?user_id=USER_ID"
```

Check the interleaving plan for concept pairing:
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/interleaving/plan?user_id=USER_ID"
```

### 5. Learn
Based on recommendations, run 3-5 exercises:
- Start with the most urgent concept
- Mix in interleaved concepts if the plan suggests it
- Alternate question types (multiple choice, short answer, teach-back)
- Keep each exercise under 60 seconds

For each question:
1. Present the question
2. Wait for the user's answer
3. Grade it (correct/incorrect + score 0-1)
4. Show explanation
5. Record result via the reflect flow

### 6. Summary
After all exercises, show:
```
Session Complete!
━━━━━━━━━━━━━━━━
Questions: 5
Correct: 4/5 (80%)
Concepts strengthened: 3
  • useEffect cleanup: 43% → 68% (+25%)
  • SQL JOINs: 52% → 52% (missed — review again tomorrow)
  • Git rebase: 61% → 78% (+17%)
Next session recommended: tomorrow at 2pm
```

### 7. Session Event
Record a session_event (type: "end") to close the session.
