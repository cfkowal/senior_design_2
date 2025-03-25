# main.py

from stepper_motor import StepperMotor
from corexy_controller import CoreXYController
from parse_hersheytext_json import load_font_from_hersheytext, draw_string
from pen_servo import HardwareServoLGPIO
from motion_planner import MotionPlanner
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

# Initialize motion planner
planner = MotionPlanner(corexy, servo)
planner.set_origin(0, 0)
planner.set_bounds(xmin=0, xmax=700, ymin=0, ymax=700)

# Read in font
font = load_font_from_hersheytext("hersheytext.json", "futural")


try:
    planner.draw_string("Free Diddy123456789", font, scale=0.5, spacing=14   )
except:
    print("\n[!] Interrupted by user.")

finally:
    print("[*] Cleaning up...")
    servo.pen_up()
    servo.close()
    motor_a.close()
    motor_b.close()
