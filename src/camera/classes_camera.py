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


class YOLOCameraManager:
    """Extends CameraManager to include YOLO object detection capabilities."""

    def __init__(self, model_path: str = "yolo12n_ncnn_model", imgz: int = 320) -> None:
        self._yolo_model: YOLO = YOLO(model_path)
        self._camera_manager: CameraManager = CameraManager()
        self._imgz = imgz

    def get_capture_and_detect_results(self):
        """Captures an image and performs object detection.

        Returns:
            The annotated image with detection results.
        """
        image = self._camera_manager.capture_image()
        image_bgr = convert_rgb_to_bgr(image)

        results = self._yolo_model.predict(image_bgr, imgz=self._imgz)

        return results

    def display_results(self) -> Any:
        """Displays the detection results on the captured image.

        Returns:
            The annotated image with detection results.
        """
        results = self.get_capture_and_detect_results()

        res = results[0] if isinstance(results, (list, tuple)) else results

        annotated_image = res.plot()

        # Display in Jupyter Notebook
        ok, buf = cv2.imencode(".jpg", annotated_image)
        if ok:
            clear_output(wait=True)
            display(Image(data=buf.tobytes()))
