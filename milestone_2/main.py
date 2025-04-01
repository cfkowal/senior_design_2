# main.py

from stepper_motor import StepperMotor
from corexy_controller import CoreXYController
from parse_hersheytext_json import load_font_from_hersheytext
from pen_servo import HardwareServoLGPIO
from motion_planner import MotionPlanner
from image_prompt_solver import ImagePromptSolver
import time
import lgpio

# Define motor pins (BCM numbers)
A_STEP = 13
A_DIR  = 10
B_STEP = 5
B_DIR  = 14
PEN_SERVO = 18

# GPIO chip
GPIO_CHIP = 0

# Stepper motor delay and steps per mm (calibrate later)
STEP_DELAY = 0.00011  # 1ms between steps
STEPS_PER_MM = 10   # depends on the belt/pulley setup

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
solver = ImagePromptSolver()





try:
    #math_response = solver.run(prompt="Solve this math problem and return only the solution.", use_camera=True, mode="math")
    #print(f"LLM RESPONSE: {math_response}")
    #planner.draw_string("A", font, scale=1, spacing=14   )
    
    planner.move_to(10, 0)
    print(planner.get_coords())
    planner.move_to(0, 0)
    print(planner.get_coords())
    
    
except:
    print("\n[!] Interrupted by user.")
    
finally:
    print("[*] Cleaning up...")
    
    servo.close()
    motor_a.close()
    motor_b.close()
