import time

class MotionPlanner:
    def __init__(self, corexy, x_switch, y_switch, servo, bounds=None):
        self.corexy = corexy
        self.servo = servo
        self.x_switch = x_switch
        self.y_switch = y_switch
        self.x = 0
        self.y = 0
        self.bounds = bounds
        self.origin = (0, 0)

    def set_origin(self, x, y):
        self.origin = (x, y)
        self.x = x
        self.y = y

    def set_bounds(self, xmin, xmax, ymin, ymax):
        self.bounds = (xmin, xmax, ymin, ymax)
        
    def get_coords(self):
        return self.x, self.y
        
    def home(self):
        self.servo.pen_up()
        while not self.x_switch.is_triggered():
                self.move_to(self.x - 1, self.y)
                #time.sleep(0.00005)
        while not self.y_switch.is_triggered():
                self.move_to(self.x, self.y - 1)
                #time.sleep(0.00005)
        
        self.move_to(self.x + 10, self.y + 10)
        self.x = 0
        self.y = 0
        
        self.corexy.set_abs_loc(self.x, self.y)
        self.set_bounds(xmin=0, xmax=190, ymin=0, ymax=240)

    def return_to_home(self):
        self.servo.pen_up()
        time.sleep(0.01)
        self.move_to(0, 0)
        
    def move_to(self, x, y):
        if self.bounds:
            xmin, xmax, ymin, ymax = self.bounds
            x = max(xmin, min(x, xmax))
            y = max(ymin, min(y, ymax))
        self.corexy.move_to(x, y)
        self.x = x
        self.y = y
        

    def transform(self, x, y):
        return x, -y 

    def draw_string(self, text, font, scale=1.0, spacing=3.0, line_height=20, space_width=1.0):
        
        #self.set_origin(self.x, self.y)
        cursor_x, cursor_y = self.x, self.y
        origin_x, origin_y = self.origin
        

        for char in text:
            self.move_to(cursor_x, cursor_y)
            if char == '\n':
                cursor_y -= line_height * scale
                cursor_x = origin_x
                continue

            if char == ' ':
                cursor_x += spacing * scale * space_width
                continue

            strokes = font.get(char)
            if not strokes:
                print(f"[!] Character '{char}' not in font")
                cursor_x += spacing * scale
                continue

            char_width = spacing * scale
            char_right = cursor_x + char_width

            if self.bounds:
                xmin, xmax, ymin, ymax = self.bounds

                if char_right > xmax:
                    cursor_y -= line_height * scale
                    cursor_x = origin_x
                    char_right = cursor_x + char_width
        
                if cursor_x < xmin:
                    print("[!] Exceeded horizontal bounds, stopping draw")
                    break

            for stroke in strokes:
                if not stroke:
                    continue

                sx, sy = stroke[0]
                rx, ry = self.transform(sx, sy)
                x0 = cursor_x + rx * scale
                y0 = cursor_y + ry * scale

                self.servo.pen_up()
                time.sleep(0.05)
                self.move_to(x0, y0)
                time.sleep(0.01)

                self.servo.pen_down(cursor_x)
                time.sleep(0.05)

                for (x, y) in stroke[1:]:
                    rx, ry = self.transform(x, y)
                    xi = cursor_x + rx * scale
                    yi = cursor_y + ry * scale
                    self.move_to(xi, yi)
                    time.sleep(0.01)

                self.servo.pen_up()
                time.sleep(0.01)

            cursor_x += char_width

        self.x = cursor_x
        self.y = cursor_y
