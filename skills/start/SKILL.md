---
name: start
description: Bootstrap Cognition — automatically installs Screenpipe, sets up auth, connects everything, and begins your first learning session. One command, zero config.
disable-model-invocation: false
---

# Start Cognition

Set up everything automatically. The user should not have to do anything manually.

## Step 1: Install & Start Screenpipe

First check if Screenpipe is already running:

```bash
curl -s http://localhost:3030/health 2>/dev/null || echo "NOT_RUNNING"
```

**If NOT running**, start it automatically in the background:

```bash
npx screenpipe@latest record > /dev/null 2>&1 &
```

Wait 5 seconds for it to initialize, then verify:

```bash
sleep 5 && curl -s http://localhost:3030/health 2>/dev/null || echo "STILL_NOT_RUNNING"
```

If it's still not running after 10 seconds, try once more. If it fails again, tell the user:
> Screenpipe couldn't start automatically. Run `npx screenpipe@latest record` in a separate terminal, then come back.

**If running**, move on.

## Step 2: Set Up Screenpipe MCP

Check if the screenpipe MCP tools are available by trying to use them. If they're not available:

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

Note: if MCP was just added, tell the user to restart this Claude Code session once for it to take effect. This only happens on first setup.

## Step 3: Auth

Check if `~/.cognition/token` exists:

```bash
cat ~/.cognition/token 2>/dev/null || echo "NO_TOKEN"
```

**If no token exists**, create one automatically for the user:

```bash
mkdir -p ~/.cognition
echo "dev-secret" > ~/.cognition/token
```

(In production, this would open a browser for OAuth signup. For now, use the dev key.)

## Step 4: Test API Connection

```bash
TOKEN=$(cat ~/.cognition/token)
curl -s -H "x-api-key: $TOKEN" https://cognition-api.fly.dev/healthz
```

If you get `{"status":"ok"}`, you're connected. If not, tell the user the API might be down and to try again in a minute.

## Step 5: First Observation

Use the screenpipe MCP tools to search recent screen content (last 30 minutes):

```
Use screenpipe search-content with content_type "ocr" and limit 10
```

Summarize what the user has been doing. Then say:

> I can see you've been working on [summary]. I'm now tracking what you're learning.
>
> Here's what I'll do:
> - Watch what you read and code via Screenpipe
> - Extract key concepts and model your knowledge
> - Quiz you on things you're about to forget
>
> Commands:
> - `/cognition:status` — see your knowledge dashboard
> - `/cognition:session` — run a study session
> - `/cognition:predict` — check what's decaying
> - `/cognition:learn` — practice right now

Then automatically ingest the recent screen content as screen_capture events via the API (use the ingest skill flow). Confirm:

> Ingested [N] screen captures. Extracted [M] concepts. Your learning model is live.

## The Goal

After running `/cognition:start`, the user should have:
1. Screenpipe running and capturing their screen
2. Screenpipe MCP connected to Claude Code
3. Auth token saved
4. API connection verified
5. First batch of screen data ingested
6. Concepts extracted and tracking started

All of this should happen automatically with ZERO user action beyond typing `/cognition:start`.
