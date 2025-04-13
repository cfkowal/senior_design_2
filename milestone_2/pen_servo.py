import lgpio
import time

class HardwareServoLGPIO:
    def __init__(self, gpio_pin, chip=0):
        self.handle = lgpio.gpiochip_open(chip)
        self.pin = gpio_pin
        self.freq = 50  
        self.up_height = 9
        lgpio.gpio_claim_output(self.handle, self.pin, 0)
        self.current_duty = self.up_height
        self.set_duty_percent(self.current_duty)
        
        self.debug_down_ht = None
        
        
    def set_down_pct(self, percent):
        self.debug_down_ht = percent
        
    def set_duty_percent(self, percent):
        """
        Set PWM duty as a percentage (e.g., 2.5 for 2.5%)
        """
        lgpio.tx_pwm(self.handle, self.pin, self.freq, percent)
    def pen_up(self):
        
        
        intervals = 5
        interval_size = (self.up_height - self.current_duty) / intervals
        
        for _ in range(intervals):
                self.set_duty_percent(self.current_duty + interval_size)
                self.current_duty = self.current_duty + interval_size
                time.sleep(0.015)

    def pen_down(self, current_X):
        
        down_height = self.calc_down_percent(current_X)
        
        #down_height = self.debug_down_ht
        
        intervals = 5
        interval_size = (self.current_duty - down_height) / intervals
        
        for _ in range(intervals):
                self.set_duty_percent(self.current_duty - interval_size)
                self.current_duty -= interval_size
                time.sleep(0.015)
                
    def calc_down_percent(self, current_X):
        slope = 0.01     
        intercept = 3.84
        
        # PEN INTERCEPT TO START 3.766
        down_pct = current_X * slope + intercept  
        
        return down_pct          
    def stop(self):
        lgpio.tx_pwm(self.handle, self.pin, self.freq, 0)

    def close(self):
        
        self.stop()
        lgpio.gpiochip_close(self.handle)
