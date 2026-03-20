# Cognition

AI that watches what you learn and helps you remember it.

## Install

Paste this into Claude Code:

```
Install Cognition by reading https://raw.githubusercontent.com/VedSoni-dev/cognition-skills/master/INSTALL.md and following every step.
```

Then restart Claude Code and type `cognition`.

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
