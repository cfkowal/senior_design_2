# stepper_motor.py

import lgpio
import time

class StepperMotor:
    def __init__(self, gpio_chip, step_pin, dir_pin, step_delay=0.001):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.step_delay = step_delay
        self.handle = lgpio.gpiochip_open(gpio_chip)

        # Claim pins as outputs
        lgpio.gpio_claim_output(self.handle, self.step_pin, 0)
        lgpio.gpio_claim_output(self.handle, self.dir_pin, 0)

    def set_direction(self, direction):
        lgpio.gpio_write(self.handle, self.dir_pin, direction)

    def step_once(self):
        lgpio.gpio_write(self.handle, self.step_pin, 1)
        time.sleep(self.step_delay)
        lgpio.gpio_write(self.handle, self.step_pin, 0)
        time.sleep(self.step_delay)

    def close(self):
        lgpio.gpiochip_close(self.handle)
