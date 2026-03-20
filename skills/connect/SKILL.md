---
name: connect
description: Connect a notification channel (Slack, Gmail, etc.) so Cognition can send you learning exercises throughout the day — even when your laptop is off.
disable-model-invocation: false
---

# Connect Notification Channel

Cognition knows exactly when your knowledge is fading. Connect a channel so it can reach you anytime.

## Step 1: Ask the user

> How should I reach you when a concept is fading?
>
> 1. **Slack** — I'll send exercises to your Slack DMs (recommended)
> 2. **Gmail** — I'll schedule emails to yourself with exercises attached
> 3. **Both** — Slack for quick probes, Gmail for full exercises

## Step 2: Set up Slack

If they choose Slack, help them add the Slack MCP:

1. Search the web for the latest Slack MCP server for Claude Code
2. Walk them through connecting it to their workspace
3. Test by sending a DM to themselves
4. Save config to `~/.cognition/notifications.json`:

```json
{
  "channels": ["slack"],
  "slack_user": "@sarah",
  "quiet_hours": {"start": 22, "end": 7},
  "max_per_day": 8
}
```

## Step 3: Set up Gmail

If they choose Gmail, help them add the Gmail MCP:

1. Search the web for the latest Gmail MCP server for Claude Code
2. Walk them through OAuth / API key setup
3. Test by sending an email to themselves
4. Save config to `~/.cognition/notifications.json`

## Step 4: Test

Send a test message through their channel with a real exercise:

**Slack example:**
```
🧠 Cognition — Quick Check

React useEffect is at 41% recall. Dropping to 12% by Friday.

**What does the cleanup function in useEffect do?**
:a: Runs when component mounts
:b: Runs on unmount or before effect re-runs
:c: Prevents re-renders
:d: Caches values

React with :a: :b: :c: or :d:

_15 seconds. Keep your knowledge alive._
```

**Gmail example:**
Subject: 🧠 3 concepts need review today

Body: full HTML exercise with interactive buttons linking to cognitionus.com/quiz
