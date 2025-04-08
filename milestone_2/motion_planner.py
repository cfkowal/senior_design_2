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
        while not self.y_switch.is_triggered():
            self.move_to(self.x, self.y - 1)

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

    def draw_string(self, text, font, scale=0.25, spacing=2.0, line_height=50, space_width=7.5):
        self.set_origin(self.x, self.y)
        cursor_x, cursor_y = self.x, self.y
        origin_x, origin_y = self.origin

        superscript_mode = False
        superscript_offset = line_height * 0.08
        superscript_scale = scale * 0.6

        i = 0
        while i < len(text):
            char = text[i]

            if char == '\n':
                cursor_y -= line_height * scale
                cursor_x = origin_x
                superscript_mode = False
                i += 1
                continue

            if char == ' ':
                cursor_x += spacing * scale * space_width
                superscript_mode = False
                i += 1
                continue

            if char == '^':
                superscript_mode = True
                i += 1
                continue

            if superscript_mode and char == '{':
                i += 1
                superscript_text = ""
                while i < len(text) and text[i] != '}':
                    superscript_text += text[i]
                    i += 1
                i += 1  # Skip closing '}'

                for sub_char in superscript_text:
                    draw_scale = superscript_scale
                    draw_y_offset = superscript_offset
                    cursor_x, _, _ = self._draw_character(sub_char, font, cursor_x, cursor_y + draw_y_offset,
                                                         draw_scale, spacing, line_height)
                superscript_mode = False
                continue

            draw_scale = superscript_scale if superscript_mode else scale
            draw_y_offset = superscript_offset if superscript_mode else 0
            cursor_x, cursor_y, _ = self._draw_character(char, font, cursor_x, cursor_y + draw_y_offset,
                                                         draw_scale, spacing, line_height)
            if superscript_mode:
                cursor_y -= draw_y_offset  # reset after superscript

            superscript_mode = False
            i += 1

    def _draw_character(self, char, font, base_x, base_y, draw_scale, spacing, line_height):
        glyph = font.get(char)
        if not glyph:
            print(f"[!] Character '{char}' not in font")
            return base_x, base_y, 0

        strokes = glyph["strokes"]
        char_advance = glyph["advance"] * spacing * draw_scale

        if self.bounds:
            xmin, xmax, ymin, ymax = self.bounds
            char_right = base_x + char_advance
            if char_right >= xmax:
                base_y -= line_height * draw_scale
                base_x = self.origin[0]
                if base_x < xmin:
                    print("[!] Exceeded horizontal bounds, stopping draw")
                    return base_x, base_y, 0

        for stroke in strokes:
            if not stroke:
                continue

            sx, sy = stroke[0]
            rx, ry = self.transform(sx, sy)
            x0 = base_x + rx * draw_scale
            y0 = base_y + ry * draw_scale

            self.servo.pen_up()
            time.sleep(0.05)
            self.move_to(x0, y0)
            time.sleep(0.01)

            self.servo.pen_down(base_x)
            time.sleep(0.05)

            for (x, y) in stroke[1:]:
                rx, ry = self.transform(x, y)
                xi = base_x + rx * draw_scale
                yi = base_y + ry * draw_scale
                self.move_to(xi, yi)
                time.sleep(0.01)

            self.servo.pen_up()
            time.sleep(0.01)

        return base_x + char_advance, base_y, char_advance
