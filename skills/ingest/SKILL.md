---
name: ingest
description: Send screen observations to the Cognition API as learning events. Transforms Screenpipe data into API event format.
user-invocable: false
---

# Ingest — Send Observations to API

Transform raw Screenpipe observations into Cognition API events and POST them.

## Steps

1. **Read the auth token:**
```bash
TOKEN=$(cat ~/.cognition/token)
```

2. **For each observation from the observe step**, construct and POST a screen_capture event:

```bash
EVENT_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
TIMESTAMP=$(python3 -c "import time; print(int(time.time()*1000))")

curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  https://cognition-api.fly.dev/v1/events \
  -d '{
    "event": {
      "schema_version": "1.0",
      "event_id": "'$EVENT_ID'",
      "idempotency_key": "'$EVENT_ID'",
      "timestamp_ms": '$TIMESTAMP',
      "event_type": "screen_capture",
      "tenant": { "tenant_id": "default", "deployment_id": "prod" },
      "user": { "user_id": "USER_ID", "pseudonymous_id": "USER_ID", "locale": "en", "timezone": "America/Chicago" },
      "session": {
        "session_id": "session-'$EVENT_ID'",
        "surface": "desktop_widget",
        "app_context": "APP_CONTEXT",
        "device": { "os": "Windows", "device_type": "desktop", "screen": { "width": 1920, "height": 1080 } },
        "attention": { "active_time_ms": 5000, "idle_time_ms": 0, "focus_switch_count": 0, "window_focus_ratio": 0.9 }
      },
      "provenance": { "source": "screen" },
      "privacy": { "consent_raw_text": true, "consent_embeddings_only": false, "pii_detected": false, "redaction_applied": false },
      "payload": {
        "text_spans": ["THE_OCR_TEXT"],
        "span_hashes": [],
        "viewport_coverage_ratio": 0.8,
        "app_context": "APP_CONTEXT",
        "concept_tagging": { "concepts": [], "edges": [], "relations": [] }
      }
    }
  }'
```

3. **Map Screenpipe app names to API AppContext:**
   - Chrome, Firefox, Edge, Safari, Arc → "Browser"
   - VS Code, Cursor, Windsurf → "VSCode"
   - Acrobat, Preview, PDF → "PDFViewer"
   - Google Docs → "GoogleDocs"
   - Everything else → "Other"

4. **Replace placeholders** with actual values:
   - `USER_ID`: from the token (decode the JWT to get the `sub` field, or use a stored user ID)
   - `APP_CONTEXT`: mapped from screenpipe app name
   - `THE_OCR_TEXT`: actual text from screenpipe

5. **Report results:**
   > Ingested 5 screen captures. API extracted 12 concepts, 4 relations.

The API handles concept extraction via Gemini and forgetting model updates automatically.
