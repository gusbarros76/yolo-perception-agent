import unittest

from api.schemas.detection import BoundingBox, DetectedObject
from api.scoring.cleanliness import compute_cleanliness_score


def _det(label: str, confidence: float) -> DetectedObject:
    return DetectedObject(
        label=label, confidence=confidence, bbox=BoundingBox(x=0, y=0, w=10, h=10)
    )


class CleanlinessScoreTestCase(unittest.TestCase):
    def test_compute_cleanliness_score_ignores_low_confidence(self):
        score, classification, breakdown = compute_cleanliness_score(
            [
                _det("bottle", 0.20),
                _det("cup", 0.10),
            ]
        )

        self.assertEqual(score, 100)
        self.assertEqual(classification, "limpo")
        self.assertEqual(breakdown.low_confidence_ignored, 2)
        self.assertEqual(breakdown.unexpected_objects, 0)

    def test_compute_cleanliness_score_applies_accumulation_penalty(self):
        score, classification, breakdown = compute_cleanliness_score(
            [
                _det("bottle", 0.90),
                _det("cup", 0.90),
                _det("book", 0.90),
            ]
        )

        self.assertEqual(score, 56)
        self.assertEqual(classification, "sujo")
        self.assertEqual(breakdown.unexpected_objects, 3)
        self.assertTrue(breakdown.accumulation_penalty_applied)


if __name__ == "__main__":
    unittest.main()
