# Typical servo pulse range (adjust if your servo differs)
SERVO_COUNTS_MAX: int = 4095  # 12-bit


# Convert angle in degrees to PCA9685 counts (0-4095)
def angle_to_counts(
    angle: float,
    angle_min: float = -180.0,
    angle_max: float = 180.0,
    servo_min_ms: float = 1.0,
    servo_max_ms: float = 2.0,
    freq: float = 50.0,
) -> int:
    """Convert an angle in degrees to 12-bit PCA9685 counts.

    Angle is clamped to [angle_min, angle_max].
    Returns an integer count in [0, 4095].
    """
    angle_deg: float = max(angle_min, min(angle_max, float(angle)))

    pulse_ms: float = servo_min_ms + (angle_deg - angle_min) / (
        angle_max - angle_min
    ) * (servo_max_ms - servo_min_ms)

    counts: int = int(pulse_ms / (1000.0 / freq) * SERVO_COUNTS_MAX)
    return counts
