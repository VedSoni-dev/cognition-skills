---
name: replay-consolidation
description: Three-phase memory replay for deep consolidation. Use when the API recommends "review" or "spaced_review" for multiple related concepts.
user-invocable: false
---

# Replay Consolidation

A structured multi-phase review that consolidates fragile memories into long-term storage.

## Steps

1. **Get the replay plan:**
```bash
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/replay/plan?user_id=USER_ID"
```

The plan has three phases:

### Phase 1: Retrieval (2-3 minutes)
- Present concepts one by one
- For each: "What do you remember about [concept]?"
- Accept free recall — don't correct yet
- Note what they remember and what they miss

### Phase 2: Consolidation (3-5 minutes)
- For each gap found in Phase 1:
  - Show the correct information
  - Connect it to something they DO remember
  - Ask a follow-up question to encode the connection
- Example:
  > You remembered that useEffect runs after render, but forgot about the cleanup function.
  > The cleanup runs when the component unmounts OR before the next effect runs.
  > Think of it like checking out of a hotel room — you clean up before the next guest arrives.
  > Quick check: If your useEffect sets up a WebSocket connection, what should the cleanup do?

### Phase 3: Spacing (1-2 minutes)
- Wait 60 seconds (have a brief conversation about something else)
- Then re-test the concepts from Phase 1 that were weak
- This immediate spaced repetition dramatically improves retention

2. **Materialize the plan** (tells the API you executed it):
```bash
curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  "https://cognition-api.fly.dev/v1/replay/materialize?user_id=USER_ID" \
  -d '{ "plan_id": "<plan_id>" }'
```

3. **Record results** for each concept via the reflect flow.

## Key Principles

- Phase 1 reveals gaps. Phase 2 fills them. Phase 3 tests if they stick.
- The 60-second delay in Phase 3 is crucial — it creates a micro-spacing effect.
- Use analogies and connections in Phase 2. Isolated facts are harder to retain.
