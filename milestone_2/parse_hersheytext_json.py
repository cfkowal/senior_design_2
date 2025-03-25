import json

# ---------- FONT PARSER ---------- #

def parse_svg_path(d_str):
    strokes = []
    current_stroke = []
    tokens = d_str.replace(',', ' ').split()
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token.startswith('M'):
            if current_stroke:
                strokes.append(current_stroke)
                current_stroke = []
            x = float(token[1:])
            y = float(tokens[i + 1])
            current_stroke.append((x, y))
            i += 2
        elif token.startswith('L'):
            x = float(token[1:])
            y = float(tokens[i + 1])
            current_stroke.append((x, y))
            i += 2
        else:
            x = float(token)
            y = float(tokens[i + 1])
            current_stroke.append((x, y))
            i += 2

    if current_stroke:
        strokes.append(current_stroke)
    return strokes


def load_font_from_hersheytext(file_path, font_name):
    with open(file_path, 'r') as f:
        data = json.load(f)

    if font_name not in data:
        raise ValueError(f"Font '{font_name}' not found in file.")

    font_data = data[font_name]["chars"]
    char_map = {}
    ascii_code = 32  # start at space

    for entry in font_data:
        d = entry["d"]
        o = entry.get("o", 0)
        strokes = parse_svg_path(d)

        # Normalize using offset 'o'
        normalized = [
            [(x - o, y) for (x, y) in stroke]
            for stroke in strokes
        ]

        char_map[chr(ascii_code)] = normalized
        ascii_code += 1

    return char_map

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
