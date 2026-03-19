---
name: observe
description: Poll Screenpipe for recent screen content and extract learning signals. Use when checking what the user has been doing on screen.
user-invocable: false
---

# Observe

Use Screenpipe MCP tools to capture what the user has been doing.

## Steps

1. **Search recent screen content** using the screenpipe `search-content` tool:
   - `content_type`: "ocr"
   - `start_time`: last known observation time (or last 15 minutes if first run)
   - `limit`: 20

2. **Filter for learning-relevant content**:
   - Reading documentation, articles, tutorials
   - Writing or editing code
   - Watching educational content
   - Browsing technical references
   - Skip: social media feeds, email inboxes, chat apps (unless learning-related)

3. **Group by context**:
   - Same app + similar content = one observation
   - Different apps = separate observations

4. **Extract key information** for each observation:
   - `text_spans`: the relevant text content
   - `app_context`: the app name (map to: Browser, VSCode, PDFViewer, GoogleDocs, Other)
   - `viewport_coverage_ratio`: estimate based on content length (0.0-1.0)
   - `timestamp_ms`: from screenpipe timestamp

5. **Return** the observations as structured data ready for ingestion via the `/cognition:ingest` flow.

## Output Format

Return a summary like:
```
Observed 5 learning events in the last 15 minutes:
1. [Browser] Reading about React hooks (3 text spans, ~45s)
2. [VSCode] Editing auth middleware (2 text spans, ~120s)
3. [Browser] Stack Overflow: "useEffect cleanup" (1 text span, ~20s)
```

Then proceed to ingest these events.
