# API

This is a minimal FastAPI service that will eventually handle perception inference and emit structured outputs for downstream consumers.

## Run locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Start server:
```bash
DETECTOR_PROVIDER=mock uvicorn main:app --reload
```

`DETECTOR_PROVIDER` options:
- `mock`: deterministic mock detector (recommended for local dev/tests)
- `yolo`: real YOLOv8 detector (`YOLO_MODEL_NAME` optional, default `yolov8n.pt`)

## Tests

```bash
PYTHONPATH=.. python -m unittest discover -s tests -v
```

## Endpoints

### `GET /health`
Healthcheck basico.

### `POST /detect`
Retorna deteccoes brutas da imagem enviada.

### `POST /detect/score`
Retorna deteccoes + score de limpeza visual + classificacao + relatorio curto.

Exemplo:
```bash
curl -X POST "http://127.0.0.1:8000/detect/score" \
  -F "file=@/caminho/imagem.jpg"
```

Resposta (exemplo):
```json
{
  "detections": [
    {
      "label": "bottle",
      "confidence": 0.81,
      "bbox": {"x": 130, "y": 240, "w": 72, "h": 110}
    }
  ],
  "score": 92,
  "classification": "sujo",
  "report": {
    "status": "sujo",
    "summary": "Foram encontrados 1 objetos de atencao.",
    "recommendation": "Ambiente sujo visualmente. Recomenda-se limpeza antes de seguir."
  },
  "breakdown": {
    "base_score": 100,
    "low_confidence_ignored": 0,
    "unexpected_objects": 1,
    "accumulation_penalty_applied": false,
    "final_score": 92
  }
}
```
