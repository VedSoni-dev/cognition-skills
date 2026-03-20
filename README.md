# Cognition

AI that watches what you learn and helps you remember it.

## Install

Paste this into Claude Code:

```
Clone https://github.com/VedSoni-dev/cognition-skills into ~/.cognition/skills, run npm install and npm link inside ~/.cognition/skills/app, install screenpipe globally with npm i -g screenpipe, add screenpipe MCP to claude code (on Windows use claude mcp add-json screenpipe '{"command":"cmd","args":["/c","npx","-y","screenpipe-mcp"],"type":"stdio"}' -s local, on Mac/Linux use claude mcp add screenpipe -- npx -y screenpipe-mcp), then tell me to restart claude code and type cognition to start.
```

Then restart Claude Code and type:

```
cognition
```

That's it. Cognition will:
- Start Screenpipe (captures your screen locally)
- Create your identity automatically
- Connect to the Cognition API
- Watch what you learn and quiz you on things you're about to forget

## Commands

| Command | What it does |
|---------|-------------|
| `/cognition:start` | Bootstrap everything |
| `/cognition:status` | Knowledge dashboard |
| `/cognition:learn` | Quiz on decaying concepts |
| `/cognition:predict` | See what's fading |
| `/cognition:session` | Full study session |

Or just talk naturally:
- "What am I forgetting?"
- "Quiz me on React hooks"
- "What was I reading earlier?"
- "How's my retention?"

## How It Works

```
You work normally
     ↓
Screenpipe captures your screen (100% local)
     ↓
Cognition API models your knowledge (Weibull forgetting curve)
     ↓
Claude Code quizzes you at the right time
     ↓
You remember more
```

## Privacy

- Screenpipe runs locally — screen data never leaves your machine
- The API receives extracted concepts, not screenshots
- Each user gets a unique ID — data is isolated
