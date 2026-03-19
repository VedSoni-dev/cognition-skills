---
name: launch
description: Launch the Cognition GUI app. Opens the Electron window and connects Claude Code to it via WebSocket. Use this after /cognition:start or whenever you need the GUI.
disable-model-invocation: false
---

# Launch Cognition GUI

## Step 1: Install dependencies (first run only)

```bash
cd ${CLAUDE_SKILL_DIR}/../../app && npm install --prefer-offline 2>/dev/null || npm install
```

## Step 2: Start the Electron app in background

```bash
cd ${CLAUDE_SKILL_DIR}/../../app && npm start > /dev/null 2>&1 &
```

Wait 3 seconds for the app to start.

## Step 3: Connect via WebSocket

Once the app is running, connect to `ws://localhost:3210` to push UI updates.

To send a message to the app, use a simple Node.js or Python script:

```bash
python3 -c "
import json, asyncio, websockets
async def send():
    async with websockets.connect('ws://localhost:3210') as ws:
        msg = json.loads(await ws.recv())  # connected message
        print('Connected to Cognition GUI')
asyncio.run(send())
" 2>/dev/null || echo "WebSocket connection ready"
```

## Step 4: Push dashboard data

After connecting, immediately push the current learner state to the dashboard:

```bash
TOKEN=$(cat ~/.cognition/token)
STATE=$(curl -s -H "x-api-key: $TOKEN" "https://cognition-api.fly.dev/v1/learner-state?user_id=vedan")

python3 -c "
import json, asyncio, websockets
async def send():
    async with websockets.connect('ws://localhost:3210') as ws:
        await ws.recv()
        await ws.send(json.dumps({'type': 'dashboard', 'data': $STATE}))
        await ws.send(json.dumps({'type': 'status', 'data': {'text': 'Session active'}}))
        print('Dashboard updated')
asyncio.run(send())
"
```

## How Claude Code uses the GUI

After launching, Claude Code can push ANY content to the app via WebSocket messages:

### Push a quiz:
```json
{"type": "quiz", "data": {
  "number": 1, "total": 5,
  "concept": "React useEffect",
  "concept_id": "react-useeffect",
  "question": "What does the cleanup function in useEffect do?",
  "choices": ["Runs on mount", "Runs on unmount or before re-run", "Prevents re-renders", "Caches values"],
  "answer": "Runs on unmount or before re-run",
  "explanation": "The cleanup function runs when the component unmounts or before the effect re-runs.",
  "image": "https://example.com/diagram.png"
}}
```

### Push a chat response:
```json
{"type": "chat-response", "data": {"text": "Great question! The aPTT test measures..."}}
```

### Push a notification:
```json
{"type": "notification", "data": {"text": "Time to review: React useEffect is decaying", "duration": 5000}}
```

### Push custom HTML (any learning technique):
```json
{"type": "custom", "data": {"html": "<h2>Teach-Back Exercise</h2><p>Explain useEffect in your own words...</p>"}}
```

### Update dashboard:
```json
{"type": "dashboard", "data": {"concept_states": [...]}}
```

## Listening for user input

The app sends messages BACK to Claude Code via WebSocket when the user:
- Answers a quiz: `{"type": "quiz-answer", "concept": "...", "correct": true, "chosen": "..."}`
- Sends a chat message: `{"type": "chat-message", "text": "..."}`
- Clicks a notification: `{"type": "notification-clicked"}`

Claude Code should listen for these and respond accordingly (record to API, generate next question, etc).
