# Imports
import time
from typing import Any

# --- HARDWARE MOCKING LOGIC ---
try:
    import Adafruit_PCA9685

    IS_HARDWARE_AVAILABLE = True

except ImportError:
    IS_HARDWARE_AVAILABLE = False

    # Create a mock class so the rest of your code doesn't crash
    class MockPCA9685:
        def __init__(self, address=0x40, busnum=1):
            print(f"[MOCK] Initialized PCA9685 at {hex(address)} on bus {busnum}")

        def set_pwm_freq(self, freq):
            print(f"[MOCK] PWM Frequency set to {freq}Hz")

        def set_pwm(self, channel, on, off):
            # 'off' is the PWM count (angle)
            print(f"[MOCK] Channel {channel} -> PWM Count: {off}")

    # Create a fake module-like object
    class FakeModule:
        PCA9685 = MockPCA9685

    Adafruit_PCA9685 = FakeModule()

from src.servo.helpers_servo import angle_to_counts

# Set the I2C bus number and PCA9685 address
# Run `i2cdetect -y -r <bus>` to find the hex address (e.g., 0x40)
I2C_BUS: int = 1
PCA9685_I2C_ADDRESS: int = 0x40


class ServoController:
    """
    Controller for a single servo connected to PCA9685.
    Naming conventions: type-first tokens for attributes (e.g., ``pos_channel``,
    ``pos_current_angle``) and full type hints on attributes and methods.
    """

    def __init__(
        self,
        channel: int = 0,
        center_angle: float = 90.0,
        freq: float = 50.0,
    ) -> None:
        self._channel: int = channel
        self._center_angle: float = center_angle
        self._current_angle: float = center_angle
        self._freq: float = freq

        self._step_dt = 1 / self._freq

        self.initialize_driver()

        # Move servo to the initial center position
        self.move_to_center(speed_deg_per_sec=30.0)

    def initialize_driver(self) -> None:
        """Initialize the PCA9685 driver for servo control."""

        self._drv_pwm: Any
        try:
            self._drv_pwm = Adafruit_PCA9685.PCA9685(
                address=PCA9685_I2C_ADDRESS, busnum=I2C_BUS
            )
            self._drv_pwm.set_pwm_freq(self._freq)  # 50 Hz is typical for servos
            print("PCA9685 initialized successfully")

        except Exception as exc:
            # If the mock fails or real hardware is missing and no mock exists
            print(f"Hardware Error: {exc}")
            raise RuntimeError("Failed to initialize PCA9685") from exc

    def move_to_center(self, **kwargs) -> None:
        """Move servo to its center position and update state."""
        # self._drv_pwm.set_pwm(self._pos_channel, 0, angle_to_counts(self._pos_center))
        self.move_to(self._center_angle, **kwargs)
        self._current_angle = self._center_angle

    def move_to(
        self,
        target_angle: float,
        speed_deg_per_sec: float = 30.0,
    ) -> None:
        """
        Move servo to ``target_angle`` at ``speed_deg_per_sec`` using steps of ``dt_step`` seconds.
        """
        start_angle: float = self._current_angle
        delta: float = float(target_angle - start_angle)
        duration: float = (
            abs(delta) / float(speed_deg_per_sec) if speed_deg_per_sec > 0 else 0.0
        )

        steps: int = max(1, int(duration / self._step_dt))
        dt: float = duration / steps

        for i_step in range(1, steps + 1):
            middle_target_angle: float = start_angle + delta * (i_step / steps)

            self._drv_pwm.set_pwm(
                self._channel, 0, angle_to_counts(middle_target_angle)
            )
            self._current_angle = middle_target_angle

            time.sleep(dt)

    def move_by_angle(self, delta_angle: float, **kwargs) -> None:
        """Move servo by ``delta_angle`` degrees from its current position."""
        target_angle: float = self._current_angle + delta_angle
        self.move_to(target_angle, **kwargs)


class DualServoController:
    """
    Controller for two servos (e.g., pan and tilt) connected to PCA9685.
    Horizontal is servo_horizontal (pan), Vertical is servo_vertical (tilt).
    """

    def __init__(
        self,
        channel_horizontal: int = 0,
        channel_vertical: int = 1,
        center_angle_horizontal: float = 90.0,
        center_angle_vertical: float = 90.0,
        freq: float = 50.0,
    ) -> None:
        self._servo_horizontal: ServoController = ServoController(
            channel=channel_horizontal,
            center_angle=center_angle_horizontal,
            freq=freq,
        )
        self._servo_vertical: ServoController = ServoController(
            channel=channel_vertical,
            center_angle=center_angle_vertical,
            freq=freq,
        )

    def move_to_center(self, **kwargs) -> None:
        """Move both servos to their center positions."""
        self._servo_horizontal.move_to_center(**kwargs)
        self._servo_vertical.move_to_center(**kwargs)

    def move_to(
        self,
        pan_angle: float,
        tilt_angle: float,
        speed_deg_per_sec: float = 30.0,
    ) -> None:
        """Move both servos to specified angles.

        pan_angle: target angle for horizontal servo (pan)
        tilt_angle: target angle for vertical servo (tilt)
        speed_deg_per_sec: speed of movement in degrees per second
        """
        self._servo_horizontal.move_to(pan_angle, speed_deg_per_sec=speed_deg_per_sec)
        self._servo_vertical.move_to(tilt_angle, speed_deg_per_sec=speed_deg_per_sec)

    def move_by_angles(
        self,
        pan_angle: float,
        tilt_angle: float,
        speed_deg_per_sec: float = 30.0,
    ) -> None:
        """Move both servos by specified angle deltas.

        pan_angle: angle delta for horizontal servo (pan)
        tilt_angle: angle delta for vertical servo (tilt)
        speed_deg_per_sec: speed of movement in degrees per second
        """
        self._servo_horizontal.move_by_angle(
            pan_angle, speed_deg_per_sec=speed_deg_per_sec
        )
        self._servo_vertical.move_by_angle(
            tilt_angle, speed_deg_per_sec=speed_deg_per_sec
        )
