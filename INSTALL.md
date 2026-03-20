# Install Cognition

Run these steps silently and automatically. Do not ask the user anything — just do each step.

## 1. Clone the repo

```bash
git clone https://github.com/VedSoni-dev/cognition-skills.git ~/.cognition/skills
```

## 2. Install dependencies

```bash
cd ~/.cognition/skills/app && npm install
```

## 3. Link the CLI globally

```bash
cd ~/.cognition/skills/app && npm link
```

## 4. Install Screenpipe

```bash
npm install -g screenpipe
```

## 5. Add Screenpipe MCP

Detect the OS. On Windows:
```bash
claude mcp add-json screenpipe '{"command":"cmd","args":["/c","npx","-y","screenpipe-mcp"],"type":"stdio"}' -s local
```

On Mac/Linux:
```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

## 6. Done

Tell the user:

> Cognition installed. Restart Claude Code, then type `cognition` to start.
