---
name: connect
description: Connect a notification channel (SMS, WhatsApp, Slack, Discord, Email) so Cognition can reach you throughout the day — not just when Claude Code is open.
disable-model-invocation: false
---

# Connect Notification Channel

Cognition knows exactly when your knowledge is fading. But it can only help if it can reach you. This skill connects a messaging channel so Cognition can send you quick checks throughout the day.

## Step 1: Ask the user

> How should I reach you when a concept is fading? Pick a channel:
>
> 1. **SMS** — Text messages (needs Twilio MCP)
> 2. **WhatsApp** — WhatsApp messages (needs Twilio or WhatsApp MCP)
> 3. **Slack** — DMs in Slack (needs Slack MCP)
> 4. **Discord** — DMs in Discord (needs Discord MCP)
> 5. **Email** — Email notifications (needs email MCP)
> 6. **Desktop** — Native OS notifications (no MCP needed, but only works on this machine)

## Step 2: Set up the MCP

Based on their choice, help them add the right MCP server to Claude Code. Search the web for the latest MCP server for their chosen channel:

- SMS/WhatsApp: Search for "Twilio MCP server claude code"
- Slack: Search for "Slack MCP server claude code"
- Discord: Search for "Discord MCP server claude code"
- Email: Search for "email MCP server claude code" or "Gmail MCP server"
- Desktop: No MCP needed — use Screenpipe's `send-notification` tool

Guide them through connecting it. They'll need their own API keys (Twilio account, Slack workspace, etc).

## Step 3: Save the preference

Save their channel preference to `~/.cognition/notifications.json`:

```json
{
  "channel": "sms",
  "phone": "+1234567890",
  "enabled": true,
  "quiet_hours": {"start": 22, "end": 7},
  "max_per_day": 10
}
```

## Step 4: Test it

Send a test message through their chosen channel:

> 🧠 Cognition connected! You'll get a message here when it's time to review something.

## Step 5: Set up the background poller

Create a scheduled task that polls the API for recommendations and sends notifications. Use Claude Code's `/loop` skill:

```
/loop 30m Check Cognition recommendations: read ~/.cognition/token for the API key, call GET https://cognition-api.fly.dev/v1/recommendations?user_id=USER_ID&limit=3, and if any have priority "urgent" or "high", send a message through the connected channel with the concept name and a quick quiz question. Format: "🧠 [Concept] is fading (43% recall). Quick: [question]? Reply A/B/C/D"
```

Or for desktop notifications (no MCP needed), use Screenpipe's built-in notification:

```bash
# Poll and notify
TOKEN=$(cat ~/.cognition/token)
RECS=$(curl -s -H "x-api-key: $TOKEN" "https://cognition-api.fly.dev/v1/recommendations?user_id=USER_ID&limit=1")
# If urgent, send desktop notification via Screenpipe
```

Use the screenpipe `send-notification` MCP tool to push native OS notifications.

## How It Works After Setup

```
User is working (Claude Code may or may not be open)
     │
     ▼
Every 30 min, background poller checks API:
  GET /v1/recommendations → any urgent?
     │
     ├── Nothing urgent → do nothing
     │
     └── "React useEffect at 41%" → Send via their channel:
              │
              ├── SMS: "🧠 useEffect fading. What does cleanup do? A) runs on mount B) runs on unmount C) prevents rerenders D) caches values"
              ├── Slack: Same, as a DM
              ├── Desktop: Native toast notification
              │
              └── User replies "B" → Record to API → stability updated
```

## Key Rules

- **Respect quiet hours.** Never notify between 10pm-7am (or their preference).
- **Max 10/day.** Don't spam. Quality over quantity.
- **Only urgent/high priority.** Low priority waits for a study session.
- **Keep it brief.** One question. 15 seconds. That's it.
- **Make replying easy.** A/B/C/D for multiple choice. Yes/No for probes.
