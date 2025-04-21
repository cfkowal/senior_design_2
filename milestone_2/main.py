# main.py

from stepper_motor import StepperMotor
from corexy_controller import CoreXYController
from parse_hersheytext_json import load_font_from_hersheytext
from pen_servo import HardwareServoLGPIO
from motion_planner import MotionPlanner
from limit_switch import LimitSwitch
from image_prompt_solver import ImagePromptSolver
from plotter_io import PlotterIO
import time
import lgpio

# Define motor pins (BCM numbers)
A_STEP = 26
A_DIR  = 10
B_STEP = 5
B_DIR  = 14
LIMIT_X = 2
LIMIT_Y = 3
PEN_SERVO = 18
START_BUTTON = 17 # ACTIVE HIGH
ERROR_LED = 6
SOLVING_LED = 27 # ACTIVE HIGH
WRITING_LED = 22

# GPIO chip
GPIO_CHIP = 0

# Stepper motor delay and steps per mm (calibrate later)
STEP_DELAY = 0.00011
STEPS_PER_MM = 19.6   # depends on the belt/pulley setup

# Initialize motors and controller
motor_a = StepperMotor(GPIO_CHIP, A_STEP, A_DIR, STEP_DELAY)
motor_b = StepperMotor(GPIO_CHIP, B_STEP, B_DIR, STEP_DELAY)
corexy = CoreXYController(motor_a, motor_b, steps_per_mm=STEPS_PER_MM)
servo = HardwareServoLGPIO(PEN_SERVO) 

# Initialize limit switches
limit_x = LimitSwitch(LIMIT_X, GPIO_CHIP)
limit_y = LimitSwitch(LIMIT_Y, GPIO_CHIP)

# Initialize motion planner
planner = MotionPlanner(corexy, limit_x, limit_y, servo)

# Initialize plotter io
io = PlotterIO(GPIO_CHIP, START_BUTTON, ERROR_LED, SOLVING_LED, WRITING_LED)

# Read in font
font = load_font_from_hersheytext("hersheytext.json", "futural")
solver = ImagePromptSolver()


try:
    
    planner.home()
    
    while True:
        io.wait_for_press()
        io.set_led("solving", True)
        ans, error = solver.run()
        io.set_led("solving", False)
        
        if not error:
            print(ans)
            io.set_led("writing", True)
            planner.move_to(20, 110)
            planner.draw_string(ans, font)
            io.set_led("writing", False)
            planner.return_to_home()

        else:
            print("Error")
            io.blink("error")
    
    
    """
    planner.home()
    planner.move_to(30, 40)
    planner.draw_string("abcdefghijklmnopqrstuvwxyz123456789", font)
    """
    
    
except Exception as e:
    print("EXCEPTION")
    print(e)
    io.blink("error")
    
finally:
    planner.return_to_home()
    servo.close()
    motor_a.close()
    motor_b.close()
    io.close()
