# Typical servo pulse range (adjust if your servo differs)
SERVO_COUNTS_MAX: int = 4096  # 12-bit


# Convert angle in degrees to PCA9685 counts (0-4095)
def angle_to_counts(
    angle: float,
    min_angle: float = 0.0,
    max_angle: float = 180.0,
    # These values now match your 145 and 605 count observations:
    servo_min_ms: float = 0.708,
    servo_max_ms: float = 2.954,
    freq: float = 50.0,
) -> int:
    """
    Convert an angle in degrees to 12-bit PCA9685 counts.

    Angle is clamped to [min_angle, max_angle].
    Returns an integer count in [0, 4095].

    ** Explanation: **
    Specifically, a servo motor determines its position based on the duration of
    an electrical pulse (Pulse Width). Here is the breakdown:

    1. The Language of Servos: Pulse Width Modulation (PWM)
        Standard servos expect a pulse every 20 milliseconds (freq = 50Hz).
        Based on hardware testing for this specific motor:
            * A 0.708ms pulse moves the servo to its minimum (0 degrees).
            * A 2.954ms pulse moves the servo to its maximum (180 degrees).
        The variable pulse_ms calculates the exact timing needed for a specific angle
        using linear interpolation.

    2. The Language of the Controller: PCA9685 Counts
        The PCA9685 chip is a 12-bit controller. It divides one full cycle (the period)
        into 4096 equal slices (0 to 4095). To generate a pulse of pulse_ms, we must
        calculate how many of these "slices" (counts) fit into that duration.

    3. Deconstructing the Math
        Formula: counts = int(pulse_ms / (1000.0 / freq) * SERVO_COUNTS_MAX)

        * 1000.0 / freq: The total Period in ms. At 50Hz, this is 20.0ms.
        * pulse_ms / 20.0: The percentage of the total cycle the pulse occupies.
          For your min angle: 0.708ms / 20.0ms = 0.0354 (3.54% duty cycle).
        * SERVO_COUNTS_MAX: We multiply that percentage by 4096 to get the hardware count.
          0.0354 * 4096 = 145 counts.
          0.1477 * 4096 = 605 counts.
    """
    # 1. Clamp the angle
    angle_deg: float = max(min_angle, min(max_angle, float(angle)))

    # 2. Map angle to pulse duration (ms)
    pulse_ms: float = servo_min_ms + (angle_deg - min_angle) / (
        max_angle - min_angle
    ) * (servo_max_ms - servo_min_ms)

    # 3. Convert ms to hardware counts
    # (pulse_ms / period_ms) * 4096
    counts: int = int(pulse_ms / (1000.0 / freq) * SERVO_COUNTS_MAX)
    return counts
