from io import BytesIO

import numpy as np
from PIL import Image
from ultralytics import YOLO

from api.inference.base import Detector
from api.schemas.detection import BoundingBox, DetectedObject


class YoloDetector(Detector):
    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = YOLO(model_name)
        self.model.to("cpu")

    def detect(self, image_bytes: bytes) -> list:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        np_image = np.array(image)
        results = self.model.predict(source=np_image, verbose=False, device="cpu")

        detections = []
        if not results:
            return detections

        result = results[0]
        boxes = result.boxes
        if boxes is None:
            return detections

        names = result.names or self.model.names
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else names[cls_id]
            detections.append(
                DetectedObject(
                    label=label,
                    confidence=conf,
                    bbox=BoundingBox(
                        x=int(x1),
                        y=int(y1),
                        w=int(x2 - x1),
                        h=int(y2 - y1),
                    ),
                )
            )

        return detections
