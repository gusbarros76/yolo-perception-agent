from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class DetectedObject(BaseModel):
    label: str
    confidence: float
    bbox: BoundingBox


class DetectionResponse(BaseModel):
    detections: list[DetectedObject]


class ScoreBreakdownResponse(BaseModel):
    base_score: int
    low_confidence_ignored: int
    unexpected_objects: int
    accumulation_penalty_applied: bool
    final_score: int


class AnalysisReportResponse(BaseModel):
    status: str
    summary: str
    recommendation: str


class DetectionAssessmentResponse(BaseModel):
    detections: list[DetectedObject]
    score: int
    classification: str
    report: AnalysisReportResponse
    breakdown: ScoreBreakdownResponse
