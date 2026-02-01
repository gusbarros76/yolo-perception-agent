from fastapi import FastAPI, File, UploadFile

from api.inference.mock import MockDetector
from api.schemas.detection import DetectionResponse

app = FastAPI(title="yolo-perception-agent")

detector = MockDetector()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    detections = detector.detect(image_bytes)
    return DetectionResponse(detections=detections)
