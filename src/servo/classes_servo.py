class ServoController:
    """Controller for a single servo connected to PCA9685.

    Naming conventions: type-first tokens for attributes (e.g., ``pos_channel``,
    ``pos_current_angle``) and full type hints on attributes and methods.
    """

    def __init__(self, drv_pwm: Any, pos_channel: int, pos_center: int = 90) -> None:
        self.drv_pwm: Any = drv_pwm
        self.pos_channel: int = pos_channel
        self.pos_center: int = pos_center
        self.pos_current_angle: int = pos_center  # assume starting at center
        # Move servo to the initial center position
        self.drv_pwm.set_pwm(self.pos_channel, 0, angle_to_counts(self.pos_current_angle))

    def move_to_center(self) -> None:
        """Move servo to its center position and update state."""
        self.drv_pwm.set_pwm(self.pos_channel, 0, angle_to_counts(self.pos_center))
        self.pos_current_angle = self.pos_center

    def move_to(self, target_angle: int, speed_deg_per_sec: float = 60.0, step_dt: float = 0.02) -> None:
        """Move servo to ``target_angle`` at ``speed_deg_per_sec`` using steps of ``step_dt`` seconds.

        This method updates ``pos_current_angle`` when the motion completes.
        """
        start_angle: int = self.pos_current_angle
        delta: float = float(target_angle - start_angle)
        duration: float = abs(delta) / float(speed_deg_per_sec) if speed_deg_per_sec > 0 else 0.0
        if duration <= 0.0:
            # Immediate move
            self.drv_pwm.set_pwm(self.pos_channel, 0, angle_to_counts(target_angle))
            self.pos_current_angle = target_angle
            return

        steps: int = max(1, int(duration / step_dt))
        dt: float = duration / steps
        for step_idx in range(1, steps + 1):
            angle_deg: float = start_angle + delta * (step_idx / steps)
            self.drv_pwm.set_pwm(self.pos_channel, 0, angle_to_counts(angle_deg))
            time.sleep(dt)
        self.pos_current_angle = target_angle