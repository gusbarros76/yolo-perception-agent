import unittest
import asyncio
from io import BytesIO

from fastapi import HTTPException
from PIL import Image
from starlette.datastructures import Headers, UploadFile

from api.main import detect, detect_score, health
from api.schemas.detection import BoundingBox, DetectedObject


class FakeDetector:
    def detect(self, image_bytes: bytes) -> list[DetectedObject]:
        return [
            DetectedObject(
                label="bottle",
                confidence=0.91,
                bbox=BoundingBox(x=10, y=20, w=30, h=40),
            )
        ]


def _make_png_bytes() -> bytes:
    image = Image.new("RGB", (16, 16), color=(255, 255, 255))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class ApiTestCase(unittest.TestCase):
    @staticmethod
    def _upload_file(filename: str, data: bytes, content_type: str) -> UploadFile:
        return UploadFile(
            file=BytesIO(data),
            filename=filename,
            headers=Headers({"content-type": content_type}),
        )

    def test_health_returns_ok(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_detect_returns_detections(self):
        response = asyncio.run(
            detect(
                file=self._upload_file("scene.png", _make_png_bytes(), "image/png"),
                detector=FakeDetector(),
            )
        )

        self.assertEqual(len(response.detections), 1)
        self.assertEqual(response.detections[0].label, "bottle")
        self.assertEqual(response.detections[0].bbox.model_dump(), {"x": 10, "y": 20, "w": 30, "h": 40})

    def test_detect_rejects_non_image_upload(self):
        with self.assertRaises(HTTPException) as exc:
            asyncio.run(
                detect(
                    file=self._upload_file("note.txt", b"not-an-image", "text/plain"),
                    detector=FakeDetector(),
                )
            )
        self.assertEqual(exc.exception.status_code, 400)
        self.assertEqual(exc.exception.detail, "Uploaded file must be an image.")

    def test_detect_rejects_corrupted_image(self):
        with self.assertRaises(HTTPException) as exc:
            asyncio.run(
                detect(
                    file=self._upload_file("broken.jpg", b"bad-bytes", "image/jpeg"),
                    detector=FakeDetector(),
                )
            )
        self.assertEqual(exc.exception.status_code, 400)
        self.assertEqual(exc.exception.detail, "Invalid or corrupted image file.")

    def test_detect_score_returns_assessment(self):
        response = asyncio.run(
            detect_score(
                file=self._upload_file("scene.png", _make_png_bytes(), "image/png"),
                detector=FakeDetector(),
            )
        )

        self.assertEqual(response.classification, "sujo")
        self.assertEqual(response.score, 92)
        self.assertEqual(response.breakdown.unexpected_objects, 1)
        self.assertEqual(response.report.status, "sujo")


if __name__ == "__main__":
    unittest.main()
