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
A_STEP = 13
A_DIR  = 10
B_STEP = 5
B_DIR  = 14
LIMIT_X = 2
LIMIT_Y = 3
PEN_SERVO = 18
START_BUTTON = 17 # ACTIVE HIGH
ERROR_LED = 6
SOLVING_LED = 27 # ACTIVE LOW
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
    
    """
    start_y = 40
    planner.home()
    
    while True:   
        # wait for button press
        io.wait_for_press()
        
        # solve
        io.set_led("solving", True)
        ans = solver.run(use_camera=True, model="gpt-4o", mode="math")
        print(ans)
        io.set_led("solving", False)
        
        # write
        io.set_led("writing", True)
        planner.move_to(55, start_y)
        planner.draw_string(ans, font, scale=0.25, spacing=2, line_height=50, space_width=7.5)
        io.set_led("writing", False)
        start_y -= 40
        planner.return_to_home()    
        """
    planner.home()
    #planner.move_to(100, 140)
    #planner.draw_string("x^{1111111111111111111111111111111}", font)
    planner.move_to(150, 190)
    planner.draw_string("x^{1111111111111111111111111111111111111111111} x + 2", font)
        
except Exception as e:
    io.set_led("error", True)
    print("ERROR")
    print(e)
    sleep(3)
    
finally:
    planner.return_to_home()
    servo.close()
    motor_a.close()
    motor_b.close()
    io.close()
