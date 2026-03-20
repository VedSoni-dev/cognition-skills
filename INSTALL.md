# Install Cognition

Paste this into Claude Code:

```
Clone https://github.com/VedSoni-dev/cognition-skills into ~/.cognition/skills, run npm install and npm link inside ~/.cognition/skills/app, install screenpipe globally with npm i -g screenpipe, add screenpipe MCP to claude code (on Windows use claude mcp add-json screenpipe '{"command":"cmd","args":["/c","npx","-y","screenpipe-mcp"],"type":"stdio"}' -s local, on Mac/Linux use claude mcp add screenpipe -- npx -y screenpipe-mcp), then tell me to restart claude code and type cognition to start.
```
