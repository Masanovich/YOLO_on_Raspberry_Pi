# Typical servo pulse range (adjust if your servo differs)
SERVO_COUNTS_MAX: int = 4095  # 12-bit


# Convert angle in degrees to PCA9685 counts (0-4095)
def angle_to_counts(
    angle: float,
    min_angle: float = 0.0,
    max_angle: float = 180.0,
    servo_min_ms: float = 1.0,
    servo_max_ms: float = 2.0,
    freq: float = 50.0,
) -> int:
    """Convert an angle in degrees to 12-bit PCA9685 counts.

    Angle is clamped to [angle_min, angle_max].
    Returns an integer count in [0, 4095].

    ** Explanation: **
    Specifically, a servo motor determines its position based on the duration of an electrical pulse.
    Here is the breakdown of why that middle step is necessary.

    1. The Language of Servos: Pulse Width Modulation (PWM)
        Standard servos expect a pulse every 20 milliseconds (which is why your freq is 50Hz).
            * A 1.0ms pulse usually tells the servo to go to its minimum position.
            * A 2.0ms pulse tells it to go to its maximum position.
        The variable pulse_ms in your code is calculating exactly how many milliseconds\
            the pulse should last to reach your desired angle.It uses linear interpolation:
            If 0° is 1ms and 180° is 2ms, then 90° must be 1.5ms.

    2. The Language of the Controller: PCA9685 Counts
        The PCA9685 chip (the hardware you're likely using) doesn't have a clock that measures milliseconds directly.
        Instead, it divides one full cycle (the "period") into 4096 equal slices (0 to 4095).
        To tell the chip to hold a pulse for pulse_ms, you have to figure out how many of those "slices" fit into that time.

    3. Deconstructing the Math
    Let's look at the final line of your code:counts = int(pulse_ms / (1000.0 / freq) * SERVO_COUNTS_MAX)
        * 1000.0 / freq: This calculates the Period (total time of one cycle) in milliseconds. At 50Hz, this is $1000 / 50 = 20ms
        * pulse_ms / 20.0 : This tells us what percentage of the total cycle the pulse takes up.
          If your pulse is 1.5ms, then $1.5 / 20.0 = 0.075$ (or 7.5% of the cycle).
        * SERVO_COUNTS_MAX: Finally, we multiply that percentage by 4095 to see how many "slices" that equals.
          0.075 \times 4095 \approx 307 counts.
    """
    angle_deg: float = max(min_angle, min(max_angle, float(angle)))

    pulse_ms: float = servo_min_ms + (angle_deg - min_angle) / (
        max_angle - min_angle
    ) * (servo_max_ms - servo_min_ms)

    counts: int = int(pulse_ms / (1000.0 / freq) * SERVO_COUNTS_MAX)
    return counts
