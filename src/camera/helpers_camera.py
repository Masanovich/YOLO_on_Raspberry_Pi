from typing import Any

import cv2


def convert_rgb_to_bgr(self, image: Any) -> Any:
    """Converts an RGB image to BGR format.

    Args:
        image: The input RGB image.

    Returns:
        The converted BGR image.
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
