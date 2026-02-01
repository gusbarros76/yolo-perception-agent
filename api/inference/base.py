from abc import ABC, abstractmethod


class Detector(ABC):
    @abstractmethod
    def detect(self, image_bytes: bytes) -> list:
        pass
