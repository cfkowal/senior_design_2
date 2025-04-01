# corexy_controller.py

from stepper_motor import StepperMotor
import time
# Bresenham's line algorithm
# Core XY controller with acceleration ramp
def move_motors_together(motor_a, motor_b, a_steps, b_steps,
                         start_delay=0.0013, min_delay=0.00011, ramp_steps=50):
    """
    Move both motors together with linear acceleration ramps.
    """

    a_dir = 1 if a_steps >= 0 else 0
    b_dir = 1 if b_steps >= 0 else 0

    motor_a.set_direction(a_dir)
    motor_b.set_direction(b_dir)

    a_steps = abs(a_steps)
    b_steps = abs(b_steps)

    a_counter = 0
    b_counter = 0
    total_steps = max(a_steps, b_steps)

    for step in range(total_steps):
        # Compute current delay for acceleration/deceleration
        if step < ramp_steps:
            # Acceleration phase
            t = step / ramp_steps
            delay = start_delay * (1 - t) + min_delay * t
        elif step > total_steps - ramp_steps:
            # Deceleration phase
            t = (total_steps - step) / ramp_steps
            delay = start_delay * (1 - t) + min_delay * t
        else:
            # Cruising phase
            delay = min_delay

        # Bresenham-style step interleaving
        if step * a_steps >= a_counter * total_steps:
            motor_a.step_once()
            a_counter += 1
        if step * b_steps >= b_counter * total_steps:
            motor_b.step_once()
            b_counter += 1

        time.sleep(delay)


class CoreXYController:
    def __init__(self, motor_a: StepperMotor, motor_b: StepperMotor, steps_per_mm=80):
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.steps_per_mm = steps_per_mm
        self.x = 0.0
        self.y = 0.0

    def move_to(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y

        dx_steps = int(dx * self.steps_per_mm)
        dy_steps = int(dy * self.steps_per_mm)

        a_steps = dx_steps + dy_steps
        b_steps = dy_steps - dx_steps

        move_motors_together(self.motor_a, self.motor_b, a_steps, b_steps)

        self.x = target_x
        self.y = target_y
