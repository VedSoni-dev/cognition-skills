---
name: schedule
description: Schedule learning exercises for the next 24 hours via Slack/Gmail. Runs at the end of every session so exercises arrive even when Claude Code is closed. The API decides WHEN and WHAT technique — you build the exercise and schedule delivery.
user-invocable: false
---

# Schedule Next-Day Reviews

This runs automatically at the end of every Cognition session. It schedules exercises for delivery via the user's connected channels (Slack, Gmail) so they arrive at the optimal time — even if the laptop is off.

## Step 1: Get upcoming reviews

```bash
TOKEN=$(cat ~/.cognition/token)
USER_ID=$(python3 -c "import json; print(json.load(open('$HOME/.cognition/identity.json'))['user_id'])")

# Get recommendations for the next 24 hours
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/recommendations?user_id=$USER_ID&limit=10"

# Get the world model plan for optimal timing
curl -s -X POST -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/world-model/plan?user_id=$USER_ID"

# Get learner strategy to pick the right techniques
curl -s -H "x-api-key: $TOKEN" \
  "https://cognition-api.fly.dev/v1/strategy/signature?user_id=$USER_ID"
```

## Step 2: Build exercises for each recommendation

For each recommendation, the API provides:
- `concept` — what needs review
- `action_type` — the learning technique to use
- `deliver_at_ms` — optimal delivery time
- `priority` — urgency level

**Build the full exercise NOW, before Claude Code closes.** Don't just schedule a reminder — schedule the actual exercise with questions, explanations, and feedback.

For each recommendation:

1. Read the `action_type` from the API
2. Build a complete exercise based on that technique:
   - `quiz` → Generate 2-3 questions with answer key and explanations
   - `teach_back` → Write a prompt asking them to explain the concept
   - `delayed_probe` → Write one focused recall question
   - `interleaving` → Mix questions from 2 concepts
   - `calibration_check` → Confidence rating + question
   - `elaborative_interrogation` → Chain of "why" questions
   - `error_correction` → Code with a bug to find
   - `practice_test` → Full mini-test with scoring
3. Format it for the delivery channel

## Step 3: Schedule via connected channels

Read `~/.cognition/notifications.json` for channel preferences.

### Slack Scheduling

For each exercise, schedule a Slack message using the Slack MCP:

**Quick probe (< 30 sec):**
```
🧠 *React useEffect* — 41% recall

What does the cleanup function in useEffect do?

:a: Runs when component mounts
:b: Runs on unmount or before effect re-runs
:c: Prevents re-renders
:d: Caches values

React with your answer. _15 seconds._

||Answer: :b: — The cleanup runs on unmount or before the next effect. Think: checking out of a hotel room before the next guest.||
```

**Teach-back (conversational):**
```
🧠 *SQL LEFT JOIN* — 38% recall

Explain LEFT JOIN to me like I'm a junior dev. What does it return when there's no match in the right table?

Reply here — I'll check your answer when you open Cognition next.
```

**Full exercise (rich):**
```
🧠 *Practice Test* — 3 concepts fading

I've prepared a 5-minute practice test:
→ cognitionus.com/quiz?session=abc123

Covers: React useEffect, SQL JOINs, Heparin
Estimated time: 4 minutes
```

Use Slack's `scheduled_send_at` or the Slack MCP's scheduling feature to set the delivery time from the API's `deliver_at_ms`.

### Gmail Scheduling

For each exercise, compose and schedule an email using the Gmail MCP:

**Subject:** 🧠 [Concept] needs review — [technique] exercise attached

**Body:** Full HTML with:
- Concept name and current recall %
- The complete exercise (questions, prompts, scenarios)
- Answer key hidden in a collapsible section or at the bottom
- Link to cognitionus.com/quiz for interactive version
- "Reply to this email with your answer" for simple probes

Use Gmail's schedule send feature to deliver at the API's recommended time.

## Step 4: Confirm to user

After scheduling, tell the user:

> 📅 Scheduled 4 reviews for tomorrow:
>
> • 10:00 AM — React useEffect (quiz via Slack)
> • 1:30 PM — SQL JOINs (teach-back via Slack)
> • 4:00 PM — Heparin (practice test via email)
> • 7:00 PM — All 3 (interleaved review via email)
>
> These will arrive even if your laptop is off. See you tomorrow.

## Step 5: Respect preferences

- Check quiet hours before scheduling
- Don't exceed max_per_day
- Space exercises at least 2 hours apart
- Urgent concepts get earlier slots
- If no channel is connected, remind them: "Run /cognition:connect to get reviews on your phone"
