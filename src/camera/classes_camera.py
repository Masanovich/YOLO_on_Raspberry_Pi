# Imports
from typing import Any

from picamera2 import Picamera2
from ultralytics import YOLO

from src.camera.helpers_camera import convert_rgb_to_bgr


class CameraManager:
    """Manager for camera operations including initialization, image capture,
    and object detection using a pre-trained YOLO model.
    """

    def __init__(self, model_path: str = "yolo12n_ncnn_model") -> None:
        self._picam2: Picamera2 = Picamera2()

        self.configure_camera()

    def configure_camera(self) -> None:
        """Configures the camera with desired settings."""
        self._picam2.configure(
            self._picam2.create_preview_configuration(
                main={"format": "XRGB8888", "size": (640, 480)}
            )
        )
        self._picam2.start()

    def capture_image(self) -> Any:
        """Captures an image from the camera.

        Returns:
            The captured image in a format suitable for processing.
        """
        return self._picam2.capture_array()


class YOLOManager:
    """Class for handling YOLO object detection on images captured from the camera."""

    def __init__(
        self,
        model_path: str = "yolo12n_ncnn_model",
        imgz: int = 320,
        device: str = "cpu",
    ) -> None:
        self._model: YOLO = YOLO(model_path)
        self._imgz: int = imgz
        self._device: str = device

    def detect_objects(self, image: Any, **kwargs) -> Any:
        """Performs object detection on the provided image.

        Args:
            image: The input image for object detection.

        Returns:
            The results of the object detection.
        """
        bgr_image: Any = convert_rgb_to_bgr(self, image)
        self._results: Any = self._model.predict(
            source=bgr_image,
            imgsz=self._imgz,
            device=self._device,
            **kwargs,
        )

    def annotate_image(self) -> Any:
        """Annotates the image with detection results.

        Returns:
            The annotated image.
        """
        annotated_image: Any = self._results[0].plot()
        return annotated_image
    
    