# yolo-perception-agent

## Project overview
A perception-first service that will take visual inputs and emit structured detection events for downstream agents.

## What the project does
- Defines a minimal API and web frontend structure for future perception workflows.
- Establishes a shared architecture and event shape for detections.

## What it does NOT do
- No YOLO inference or model execution.
- No decision-making, planning, or agent logic.
- No frontend functionality beyond initial scaffolding.

## High-level architecture
Input -> Perception -> Structured Output -> Consumption by agents.

Perception is separated from decision-making so downstream systems can interpret observations independently.

## Example detection event JSON
```json
{
  "event_id": "evt_001",
  "timestamp": "2026-02-01T00:00:00Z",
  "source": "camera/front",
  "detections": [
    {
      "label": "person",
      "confidence": 0.92,
      "bbox": {"x": 120, "y": 80, "w": 64, "h": 160}
    }
  ]
}
```

## Status
MVP in progress.
