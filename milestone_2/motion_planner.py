import time

class MotionPlanner:
    def __init__(self, corexy, servo, bounds=None):
        self.corexy = corexy
        self.servo = servo
        self.x = 0
        self.y = 0
        self.bounds = bounds  # (xmin, xmax, ymin, ymax)
        self.origin = (0, 0)

    def set_origin(self, x, y):
        """Set new origin location"""
        self.origin = (x, y)
        self.x = x
        self.y = y

    def set_bounds(self, xmin, xmax, ymin, ymax):
        """Define movement bounding box"""
        self.bounds = (xmin, xmax, ymin, ymax)

    def home(self):
        """
        Placeholder for limit-switch-based homing.
        You’ll wire this up later when switches are added.
        """
        print("[HOME] Moving to (0, 0)... (limit switches TBD)")
        self.set_origin(0, 0)
        self.move_to(0, 0)

    def move_to(self, x, y):
    # Clamp unrotated x/y to bounds
        if self.bounds:
                xmin, xmax, ymin, ymax = self.bounds
                x = max(xmin, min(x, xmax))
                y = max(ymin, min(y, ymax))

    # Store logical position
        self.x = x
        self.y = y

    # Convert to rotated position for movement
        rx, ry = -y, x
        self.corexy.move_to(rx, ry)


    def draw_string(self, text, font, scale=1.0, spacing=3.0, line_height=20, space_width=1.0):
        """
        Draw text using font and scale.
        Honors origin and bounds — skips or wraps characters that would overflow.
        space_width: width multiplier for space characters
        """
        cursor_x, cursor_y = self.x, self.y
        origin_x = self.origin[0]
        origin_y = self.origin[1]

        for char in text:
            if char == '\n':
                cursor_y += line_height * scale
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
                    cursor_y += line_height * scale
                    cursor_x = origin_x
                    char_right = cursor_x + char_width

                if cursor_y > ymax:
                    print("[!] Exceeded vertical bounds, stopping draw")
                    break

            for stroke in strokes:
                if not stroke:
                    continue

                x0 = cursor_x + stroke[0][0] * scale
                y0 = cursor_y + stroke[0][1] * scale

                self.servo.pen_up()
                time.sleep(0.05)
                self.move_to(x0, y0)
                time.sleep(0.01)

                self.servo.pen_down()
                time.sleep(0.05)

                for (x, y) in stroke[1:]:
                    xi = cursor_x + x * scale
                    yi = cursor_y + y * scale
                    self.move_to(xi, yi)
                    
                    time.sleep(0.01)

                self.servo.pen_up()
                time.sleep(0.01)

            cursor_x += char_width
            

        self.x = cursor_x
        self.y = cursor_y
