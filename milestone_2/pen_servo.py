import lgpio
import time

class HardwareServoLGPIO:
    def __init__(self, gpio_pin, chip=0):
        self.handle = lgpio.gpiochip_open(chip)
        self.pin = gpio_pin
        self.freq = 50  # 50Hz PWM for servo

        # Claim pin (optional — usually only needed for outputs)
        lgpio.gpio_claim_output(self.handle, self.pin, 0)

    def set_duty_percent(self, percent):
        """
        Set PWM duty as a percentage (e.g., 2.5 for 2.5%)
        """
        lgpio.tx_pwm(self.handle, self.pin, self.freq, percent)
    def pen_up(self):
        self.set_duty_percent(6)
    
    def pen_down(self):
        self.set_duty_percent(3)
        
    def stop(self):
        lgpio.tx_pwm(self.handle, self.pin, self.freq, 0)

    def close(self):
        self.stop()
        lgpio.gpiochip_close(self.handle)
