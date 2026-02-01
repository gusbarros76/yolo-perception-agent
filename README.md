# yolo-perception-agent

## Project overview
A perception-first service that will take visual inputs and emit structured detection events for downstream agents.

## What the project does
- Provides a minimal API and web frontend structure for perception workflows.
- Runs real-time object detection and emits structured detection events.

## What it does NOT do
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

## MVP Status
This MVP includes:
- Real object detection using YOLOv8 (CPU, Ultralytics)
- Image upload via FastAPI
- Structured detection events (JSON contract)
- Clean inference abstraction (mock -> real detector)

The MVP intentionally focuses on the perception layer only; downstream decision-making is out of scope.

Example detection response:
```json
{
  "detections": [
    {
      "label": "person",
      "confidence": 0.88,
      "bbox": {"x": 52, "y": 40, "w": 86, "h": 190}
    },
    {
      "label": "car",
      "confidence": 0.81,
      "bbox": {"x": 210, "y": 120, "w": 220, "h": 120}
    }
  ]
}
```

## Status
MVP in progress.
