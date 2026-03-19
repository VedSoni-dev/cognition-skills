---
name: reflect
description: Record learning exercise results back to the Cognition API. Updates the forgetting model.
user-invocable: false
---

# Reflect — Record Results

After any learning exercise, record the results back to the Cognition API so the forgetting model updates.

## For Quiz Answers

For each question the user answered, POST a `quiz_answer` event:

```bash
TOKEN=$(cat ~/.cognition/token)
curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  https://cognition-api.fly.dev/v1/events \
  -d '{
    "event": {
      "schema_version": "1.0",
      "event_id": "'$(python3 -c "import uuid; print(uuid.uuid4())")'",
      "idempotency_key": "'$(python3 -c "import uuid; print(uuid.uuid4())")'",
      "timestamp_ms": '$(python3 -c "import time; print(int(time.time()*1000))")',
      "event_type": "quiz_answer",
      "tenant": { "tenant_id": "TENANT_ID", "deployment_id": "prod" },
      "user": { "user_id": "USER_ID", "pseudonymous_id": "USER_ID", "locale": "en", "timezone": "America/Chicago" },
      "session": {
        "session_id": "SESSION_ID",
        "surface": "desktop_widget",
        "app_context": "Other",
        "device": { "os": "Windows", "device_type": "desktop", "screen": { "width": 1920, "height": 1080 } },
        "attention": { "active_time_ms": 5000, "idle_time_ms": 0, "focus_switch_count": 0, "window_focus_ratio": 1.0 }
      },
      "provenance": { "source": "quiz" },
      "privacy": { "consent_raw_text": true, "consent_embeddings_only": false, "pii_detected": false, "redaction_applied": false },
      "payload": {
        "quiz_session_id": "QUIZ_SESSION",
        "quiz_id": "QUIZ_ID",
        "quiz_version": "1.0",
        "question_id": "Q1",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "is_correct": true,
        "evaluation_score": 1.0,
        "latency_ms": 5000,
        "hints_used": 0,
        "solution_viewed": false,
        "kc_node_id": "CONCEPT_ID",
        "mastery_change": 0.0,
        "concept_tagging": { "concepts": ["CONCEPT_ID"] }
      }
    }
  }'
```

Replace placeholder values (TENANT_ID, USER_ID, etc.) with actual values from the current session context.

## For Delayed Probes

POST a `delayed_probe` event with the probe result:

```bash
curl -s -X POST -H "x-api-key: $TOKEN" -H "Content-Type: application/json" \
  https://cognition-api.fly.dev/v1/probes/outcome \
  -d '{
    "probe_id": "PROBE_ID",
    "concept_id": "CONCEPT_ID",
    "horizon_days": 3,
    "predicted_recall": 0.65,
    "result_correct": true,
    "result_score": 0.9,
    "result_confidence": 0.8
  }'
```

## After Recording

Confirm to the user what was updated:
- "Updated 3 concept states. useEffect cleanup stability: 3.2 → 5.8 days."
- Show the next predicted review date for each concept.
