import os
from functools import lru_cache
from io import BytesIO

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from api.inference.base import Detector
from api.inference.mock import MockDetector
from api.inference.yolo import YoloDetector
from api.schemas.detection import (
    AnalysisReportResponse,
    DetectionAssessmentResponse,
    DetectionResponse,
    ScoreBreakdownResponse,
)
from api.scoring.cleanliness import compute_cleanliness_score

app = FastAPI(title="yolo-perception-agent")


def _build_detector() -> Detector:
    provider = os.getenv("DETECTOR_PROVIDER", "yolo").strip().lower()
    if provider == "mock":
        return MockDetector()
    if provider == "yolo":
        model_name = os.getenv("YOLO_MODEL_NAME", "yolov8n.pt")
        return YoloDetector(model_name=model_name)
    raise ValueError(
        "Unsupported DETECTOR_PROVIDER. Use 'yolo' or 'mock'."
    )


@lru_cache
def get_detector() -> Detector:
    try:
        return _build_detector()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def _read_validated_image(file: UploadFile) -> bytes:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.") from exc

    return image_bytes


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect", response_model=DetectionResponse)
async def detect(
    file: UploadFile = File(...), detector: Detector = Depends(get_detector)
):
    image_bytes = await _read_validated_image(file)
    detections = detector.detect(image_bytes)
    return DetectionResponse(detections=detections)


@app.post("/detect/score", response_model=DetectionAssessmentResponse)
async def detect_score(
    file: UploadFile = File(...), detector: Detector = Depends(get_detector)
):
    image_bytes = await _read_validated_image(file)
    detections = detector.detect(image_bytes)

    score, classification, breakdown = compute_cleanliness_score(detections)

    summary = f"Foram encontrados {breakdown.unexpected_objects} objetos de atencao."

    recommendation_by_classification = {
        "limpo": "Ambiente limpo visualmente.",
        "sujo": "Ambiente sujo visualmente. Recomenda-se limpeza antes de seguir.",
    }

    report = AnalysisReportResponse(
        status=classification,
        summary=summary,
        recommendation=recommendation_by_classification[classification],
    )

    return DetectionAssessmentResponse(
        detections=detections,
        score=score,
        classification=classification,
        report=report,
        breakdown=ScoreBreakdownResponse(
            base_score=breakdown.base_score,
            low_confidence_ignored=breakdown.low_confidence_ignored,
            unexpected_objects=breakdown.unexpected_objects,
            accumulation_penalty_applied=breakdown.accumulation_penalty_applied,
            final_score=breakdown.final_score,
        ),
    )
