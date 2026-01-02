# Imports
from typing import Any
import Adafruit_PCA9685
import time

from src.servo.helpers_servo import angle_to_counts

# Set the I2C bus number and PCA9685 address
# Run `i2cdetect -y -r <bus>` to find the hex address (e.g., 0x40)
I2C_BUS: int = 1
PCA9685_I2C_ADDRESS: int = 0x40

# Servo helpers and demo
# Helpers for angle ↔ PWM counts (assumes 50 Hz)
FREQ: int = 50
PERIOD_MS: float = 1000.0 / FREQ

CHANNEL: int = 0
DEG_CENTER: int = 90


class ServoController:
    """Controller for a single servo connected to PCA9685.

    Naming conventions: type-first tokens for attributes (e.g., ``pos_channel``,
    ``pos_current_angle``) and full type hints on attributes and methods.
    """

    def __init__(self, channel: int = CHANNEL, deg_center: int = DEG_CENTER) -> None:
        self._pos_channel: int = channel
        self._pos_center: int = deg_center
        self._angle_curr: int = deg_center  # assume starting at center

        self.initialize_driver()
        # Move servo to the initial center position
        self._drv_pwm.set_pwm(
            self._pos_channel, 0, angle_to_counts(self._angle_curr)
        )

    def initialize_driver(self) -> None:
        """Initialize the PCA9685 driver for servo control."""

        self._drv_pwm: Any
        try:
            self._drv_pwm = Adafruit_PCA9685.PCA9685(
                address=PCA9685_I2C_ADDRESS, busnum=I2C_BUS
            )
            self._drv_pwm.set_pwm_freq(FREQ)  # 50 Hz is typical for servos
            print("PCA9685 initialized successfully")
        except Exception as exc:
            raise RuntimeError("Failed to initialize PCA9685") from exc

    def move_to_center(self) -> None:
        """Move servo to its center position and update state."""
        self._drv_pwm.set_pwm(self._pos_channel, 0, angle_to_counts(self._pos_center))
        self._angle_curr = self._pos_center

    def move_to(
        self, angle_target: int, speed_deg_per_sec: float = 60.0, step_dt: float = 0.02
    ) -> None:
        """Move servo to ``target_angle`` at ``speed_deg_per_sec`` using steps of ``step_dt`` seconds.

        This method updates ``angle_curr`` when the motion completes.
        """
        angle_start: int = self._angle_curr
        delta: float = float(angle_target - angle_start)
        duration: float = (
            abs(delta) / float(speed_deg_per_sec) if speed_deg_per_sec > 0 else 0.0
        )
        if duration <= 0.0:
            # Immediate move
            self._drv_pwm.set_pwm(self._pos_channel, 0, angle_to_counts(angle_target))
            self._angle_curr = angle_target
            return

        steps: int = max(1, int(duration / step_dt))
        dt: float = duration / steps
        for step_idx in range(1, steps + 1):
            angle_deg: float = angle_start + delta * (step_idx / steps)
            self._drv_pwm.set_pwm(self._pos_channel, 0, angle_to_counts(angle_deg))
            time.sleep(dt)
        self._angle_curr = angle_target
