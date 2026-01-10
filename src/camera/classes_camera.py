# Imports
from typing import Any

import cv2
from IPython.display import Image, clear_output, display
from picamera2 import Picamera2
from ultralytics import YOLO

from src.camera.helpers_camera import convert_rgb_to_bgr


class CameraManager:
    """Manager for camera operations including initialization, image capture,
    and object detection using a pre-trained YOLO model.
    """

    def __init__(self, x_size: int = 640, y_size: int = 480) -> None:
        self._picam2: Picamera2 = Picamera2()
        self._x_size: int = x_size
        self._y_size: int = y_size

        self.configure_camera()

        self._picam2.start()

    def configure_camera(self) -> None:
        """Configures the camera with desired settings."""
        self._picam2.configure(
            self._picam2.create_preview_configuration(
                main={"format": "XRGB8888", "size": (self._x_size, self._y_size)}
            )
        )

    def capture_image(self) -> Any:
        """Captures an image from the camera.

        Returns:
            The captured image in a format suitable for processing.
        """
        return self._picam2.capture_array()

    def get_xy_size(self) -> tuple[int, int]:
        """Returns the current image size as (x_size, y_size)."""
        return self._x_size, self._y_size


class YOLOCameraManager:
    """Extends CameraManager to include YOLO object detection capabilities."""

    def __init__(
        self, model_path: str = "yolo12n_ncnn_model", imgsz: int = 320
    ) -> None:
        self._yolo_model: YOLO = YOLO(model_path)
        self._camera_manager: CameraManager = CameraManager()
        self._imgsz = imgsz

    def capture_image(self) -> Any:
        """Captures an image from the camera.

        Returns:
            The captured image in a format suitable for processing.
        """
        return self._camera_manager.capture_image()

    def get_results_from_image(self, image=None, **kwargs) -> Any:
        """Captures an image and performs object detection.

        Returns:
            The annotated image with detection results.
        """
        image = self._camera_manager.capture_image() if image is None else image
        image = convert_rgb_to_bgr(image)

        results = self._yolo_model.predict(image, imgsz=self._imgsz, **kwargs)

        return results

    def get_annotated_image(self, results=None) -> Any:
        """Displays the detection results on the captured image.

        Returns:
            The annotated image with detection results.
        """
        results = self.get_results_from_image() if results is None else results

        res = results[0] if isinstance(results, (list, tuple)) else results

        annotated_image = res.plot()

        annotated_image = convert_rgb_to_bgr(annotated_image)

        return annotated_image

    def display_annotated_video(self) -> None:
        """Displays the annotated image with detection results in a Jupyter Notebook."""

        while True:
            annotated_image = self.get_annotated_image()

            clear_output(wait=True)
            display(Image(data=cv2.imencode(".jpg", annotated_image)[1].tobytes()))

    def get_camera_xy_size(self) -> tuple[int, int]:
        """Returns the current image size as (x_size, y_size)."""
        return self._camera_manager.get_xy_size()
