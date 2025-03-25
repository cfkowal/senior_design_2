import json

# ---------- FONT PARSER ---------- #

import json

def parse_stroke_data(d_string):
    strokes = []
    segments = d_string.strip().split("M")[1:]  # remove empty before first M
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        points = seg.replace("L", "").split()
        stroke = []
        for pt in points:
            if "," in pt:
                x_str, y_str = pt.split(",")
                stroke.append((float(x_str), float(y_str)))
        strokes.append(stroke)
    return strokes

def load_font_from_hersheytext(json_path, font_name):
    with open(json_path, "r") as f:
        font_data = json.load(f)

    if font_name not in font_data:
        raise ValueError(f"Font '{font_name}' not found in file.")

    raw_font = font_data[font_name]
    raw_chars = raw_font["chars"]

    # Hershey fonts typically start at ASCII 32 (space)
    ascii_offset = 33
    font = {}
    for i, char_data in enumerate(raw_chars):
        ascii_code = ascii_offset + i
        char = chr(ascii_code)
        font[char] = parse_stroke_data(char_data["d"])

    return font


# ---------- DRAW FUNCTION ---------- #

def draw_string(text, font, start_x=0, start_y=0, scale=1.0, spacing=3.0):
    cursor_x = start_x
    cursor_y = start_y

    for char in text:
        if char == '\n':
            cursor_y += 20 * scale  # basic line height
            cursor_x = start_x
            continue

        strokes = font.get(char)
        if not strokes:
            print(f"[!] Character '{char}' not in font")
            cursor_x += spacing * scale
            continue

        for stroke in strokes:
            if not stroke:
                continue
            # Pen up: move to first point
            x0 = cursor_x + stroke[0][0] * scale
            y0 = cursor_y + stroke[0][1] * scale
            print(f"[pen up] move to ({x0:.2f}, {y0:.2f})")

            print("[pen down]")
            for (x, y) in stroke[1:]:
                xi = cursor_x + x * scale
                yi = cursor_y + y * scale
                print(f"  draw to ({xi:.2f}, {yi:.2f})")
            print("[pen up]")

        # Advance cursor
        cursor_x += spacing * scale
