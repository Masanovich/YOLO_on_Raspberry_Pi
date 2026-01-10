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

    def __init__(self, model_path: str = "yolo12n_ncnn_model") -> None:
        self._picam2: Picamera2 = Picamera2()

        # self.configure_camera()

        self._picam2.start()

    def configure_camera(self) -> None:
        """Configures the camera with desired settings."""
        self._picam2.configure(
            self._picam2.create_preview_configuration(
                main={"format": "XRGB8888", "size": (640, 480)}
            )
        )

    def capture_image(self) -> Any:
        """Captures an image from the camera.

        Returns:
            The captured image in a format suitable for processing.
        """
        return self._picam2.capture_array()


class YOLOCameraManager:
    """Extends CameraManager to include YOLO object detection capabilities."""

    def __init__(
        self, model_path: str = "yolo12n_ncnn_model", imgsz: int = 320
    ) -> None:
        self._yolo_model: YOLO = YOLO(model_path)
        self._camera_manager: CameraManager = CameraManager()
        self._imgsz = imgsz

    def get_capture_and_detect_results(self):
        """Captures an image and performs object detection.

        Returns:
            The annotated image with detection results.
        """
        image = self._camera_manager.capture_image()
        image = convert_rgb_to_bgr(image)

        results = self._yolo_model.predict(image, imgsz=self._imgsz)

        return results

    def get_annotated_image(self) -> Any:
        """Displays the detection results on the captured image.

        Returns:
            The annotated image with detection results.
        """
        results = self.get_capture_and_detect_results()

        res = results[0] if isinstance(results, (list, tuple)) else results

        annotated_image = res.plot()

        # annotated_image = convert_rgb_to_bgr(annotated_image)

        return annotated_image

    def display_annotated_video(self) -> None:
        """Displays the annotated image with detection results in a Jupyter Notebook."""

        while True:
            annotated_image = self.get_annotated_image()

            clear_output(wait=True)
            display(Image(data=cv2.imencode(".jpg", annotated_image)[1].tobytes()))
