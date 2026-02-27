from dataclasses import dataclass

from api.schemas.detection import DetectedObject


@dataclass
class ScoreBreakdown:
    base_score: int
    low_confidence_ignored: int
    unexpected_objects: int
    accumulation_penalty_applied: bool
    final_score: int


def classify_score(unexpected_objects: int) -> str:
    if unexpected_objects == 0:
        return "limpo"
    return "sujo"


def compute_cleanliness_score(
    detections: list[DetectedObject], confidence_threshold: float = 0.35
) -> tuple[int, str, ScoreBreakdown]:
    # Common COCO classes that may indicate visual clutter in a floor/bench scenario.
    clutter_labels = {
        "bottle",
        "cup",
        "wine glass",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "dining table",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "book",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "sports ball",
        "skateboard",
    }

    score = 100
    low_confidence_ignored = 0
    unexpected_objects = 0

    for det in detections:
        if det.confidence < confidence_threshold:
            low_confidence_ignored += 1
            continue

        if det.label in clutter_labels:
            unexpected_objects += 1
            score -= 8

    accumulation_penalty_applied = unexpected_objects >= 3
    if accumulation_penalty_applied:
        score -= 20

    final_score = max(0, min(100, score))
    classification = classify_score(unexpected_objects)

    breakdown = ScoreBreakdown(
        base_score=100,
        low_confidence_ignored=low_confidence_ignored,
        unexpected_objects=unexpected_objects,
        accumulation_penalty_applied=accumulation_penalty_applied,
        final_score=final_score,
    )

    return final_score, classification, breakdown
