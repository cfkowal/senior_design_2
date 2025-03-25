# main.py

from stepper_motor import StepperMotor
from corexy_controller import CoreXYController
from parse_hersheytext_json import load_font_from_hersheytext, draw_string
from pen_servo import HardwareServoLGPIO
import time
import lgpio

# Define motor pins (BCM numbers)
A_STEP = 13
A_DIR  = 10
B_STEP = 5
B_DIR  = 14
PEN_SERVO = 18

# GPIO chip (check gpioinfo, usually 0 or 4 on Pi 5)
GPIO_CHIP = 0

# Stepper motor delay and steps per mm (calibrate later)
STEP_DELAY = 0.00011  # 1ms between steps
STEPS_PER_MM = 10   # depends on your belt/pulley setup

# Initialize motors and controller
motor_a = StepperMotor(GPIO_CHIP, A_STEP, A_DIR, STEP_DELAY)
motor_b = StepperMotor(GPIO_CHIP, B_STEP, B_DIR, STEP_DELAY)
corexy = CoreXYController(motor_a, motor_b, steps_per_mm=STEPS_PER_MM)
servo = HardwareServoLGPIO(18)  # BCM pin 18 on Pi 5 = GPIO line 18


try:
    font = load_font_from_hersheytext("hersheytext.json", "timesr")

    servo.pen_up()
    time.sleep(1)
    
    corexy.move_to(100, 100)
    servo.pen_down()
    time.sleep(1)
    corexy.move_to(0, 0)
    servo.pen_up()
finally:
    motor_a.close()
    motor_b.close()
    servo.close()
    print("GPIOs released.")
