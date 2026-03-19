# Cognition Skills

AI that watches what you learn and helps you remember it. Powered by the [Cognition API](https://cognition-api.fly.dev).

## Quick Start

### 1. Install Screenpipe MCP

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

### 2. Install the Cognition plugin

```bash
claude --plugin-dir /path/to/cognition-skills
```

Or install from the marketplace:
```
/plugin install https://github.com/cognition-labs/cognition-skills
```

### 3. Start Cognition

```
/cognition:start
```

This will:
- Check your Screenpipe connection
- Set up authentication
- Begin observing what you're learning

## Commands

| Command | What it does |
|---------|-------------|
| `/cognition:start` | Bootstrap — set up auth and begin |
| `/cognition:status` | Show your knowledge dashboard |
| `/cognition:predict` | Check what's decaying |
| `/cognition:session` | Run a full study session |
| `/cognition:learn` | Generate a learning exercise |

## How It Works

```
Screenpipe → observes your screen
     ↓
Cognition API → models what you know (Weibull forgetting curve)
     ↓
Claude → generates personalized learning exercises
     ↓
You → answer questions, build lasting knowledge
```

## Learning Techniques

Cognition uses six evidence-based learning techniques:

- **Spaced Retrieval** — Active recall at optimal intervals
- **Interleaving** — Mix related concepts for deeper discrimination
- **Delayed Probes** — Quick surprise retention checks
- **Replay Consolidation** — Three-phase memory consolidation
- **Teach-Back** — Explain concepts to prove mastery
- **Calibration Checks** — Align confidence with actual knowledge

The system picks the right technique based on your learning profile, concept state, and the API's world model rollouts.

## Architecture

No API keys needed. No separate app to install.

- **Screenpipe** captures your screen (local, private)
- **Cognition API** runs the learning algorithms (cloud)
- **Claude Code** orchestrates everything and generates exercises
- **Skills** are loaded dynamically from this repo

## Privacy

- Screenpipe runs 100% locally — your screen data never leaves your machine
- The Cognition API receives extracted text and concepts, not screenshots
- All data is per-user, tenant-isolated
