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
                x = float(x_str)
                y = float(y_str)
                stroke.append((x, y))  # ✅ Use direct x, y (no rotation)
        strokes.append(stroke)
    return strokes

def load_font_from_hersheytext(json_path, font_name):
    with open(json_path, "r") as f:
        font_data = json.load(f)

    if font_name not in font_data:
        raise ValueError(f"Font '{font_name}' not found in file.")

    raw_font = font_data[font_name]
    raw_chars = raw_font["chars"]

    ascii_offset = 33
    font = {}
    for i, char_data in enumerate(raw_chars):
        ascii_code = ascii_offset + i
        char = chr(ascii_code)
        font[char] = parse_stroke_data(char_data["d"])

    return font
