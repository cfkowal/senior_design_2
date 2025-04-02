# main.py

from stepper_motor import StepperMotor
from corexy_controller import CoreXYController
from parse_hersheytext_json import load_font_from_hersheytext
from pen_servo import HardwareServoLGPIO
from motion_planner import MotionPlanner
from limit_switch import LimitSwitch
from image_prompt_solver import ImagePromptSolver
import time
import lgpio

# Define motor pins (BCM numbers)
A_STEP = 13
A_DIR  = 10
B_STEP = 5
B_DIR  = 14
LIMIT_X = 2
LIMIT_Y = 3
PEN_SERVO = 18

# GPIO chip
GPIO_CHIP = 0

# Stepper motor delay and steps per mm (calibrate later)
STEP_DELAY = 0.00011  # 1ms between steps
STEPS_PER_MM = 19.6   # depends on the belt/pulley setup

# Initialize motors and controller
motor_a = StepperMotor(GPIO_CHIP, A_STEP, A_DIR, STEP_DELAY)
motor_b = StepperMotor(GPIO_CHIP, B_STEP, B_DIR, STEP_DELAY)
corexy = CoreXYController(motor_a, motor_b, steps_per_mm=STEPS_PER_MM)
servo = HardwareServoLGPIO(18)  # BCM pin 18 on Pi 5 = GPIO line 18

# Initialize limit switches
limit_x = LimitSwitch(LIMIT_X, GPIO_CHIP)
limit_y = LimitSwitch(LIMIT_Y, GPIO_CHIP)

# Initialize motion planner
planner = MotionPlanner(corexy, limit_x, limit_y, servo)
#planner.set_origin(0, 0)

# Read in font
font = load_font_from_hersheytext("hersheytext.json", "futural")
solver = ImagePromptSolver()



# NEED TO SET ORIGIN WHEN START WRITING ANSWER, IMPORTANT FOR LINE SPACING

try:
    
    planner.home()
    planner.move_to(60, 50)
    planner.draw_string("1 2 3 4 5 6 7 8", font=font, scale=0.4, spacing=13, line_height=20, space_width=1.0)

    
except:
    print("\n[!] Interrupted by user.")
    
finally:
    print("[*] Cleaning up...")
    
    servo.pen_up()
    servo.close()
    motor_a.close()
    motor_b.close()
