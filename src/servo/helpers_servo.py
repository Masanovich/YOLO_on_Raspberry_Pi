# Typical servo pulse range (adjust if your servo differs)
SERVO_MIN_MS: float = 1.0  # ms for min angle
SERVO_MAX_MS: float = 2.0  # ms for max angle
ANGLE_MIN: int = 0
ANGLE_MAX: int = 180


# Convert angle in degrees to PCA9685 counts (0-4095)
def angle_to_counts(
    angle: float,
    angle_min: int = ANGLE_MIN,
    angle_max: int = ANGLE_MAX,
    servo_min_ms: float = SERVO_MIN_MS,
    servo_max_ms: float = SERVO_MAX_MS,
    freq: int = 50,
) -> int:
    """Convert an angle in degrees to 12-bit PCA9685 counts.

    Angle is clamped to [angle_min, angle_max].
    Returns an integer count in [0, 4095].
    """
    angle_deg: float = max(angle_min, min(angle_max, float(angle)))
    pulse_ms: float = servo_min_ms + (angle_deg - angle_min) / (
        angle_max - angle_min
    ) * (servo_max_ms - servo_min_ms)
    counts: int = int(pulse_ms / (1000.0 / freq) * 4096)
    return counts
