from api.inference.base import Detector
from api.schemas.detection import BoundingBox, DetectedObject


class MockDetector(Detector):
    def detect(self, image_bytes: bytes) -> list:
        return [
            DetectedObject(
                label="person",
                confidence=0.92,
                bbox=BoundingBox(x=120, y=80, w=64, h=160),
            )
        ]
