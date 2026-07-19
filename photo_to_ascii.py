#!/usr/bin/env python3
"""
Turns a photo into the ASCII portrait shown on the left of the profile card.

Run this ONLY when you want to change the photo:
    python3 photo_to_ascii.py avatar.jpg

It writes portrait.txt, which generate_profile.py reads.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

SRC = sys.argv[1] if len(sys.argv) > 1 else "avatar.jpg"
COLS = 96
ASPECT = 1.72        # svg line-height / char-width
RAMP = "@%#*+=-:. "  # darkest -> lightest

def main():
    img = Image.open(SRC).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)

    w, h = img.size
    rows = int(COLS * (h / w) / ASPECT)

    img_resized = img.resize((COLS, rows), Image.LANCZOS)
    n = len(RAMP) - 1

    lines = []
    for y in range(rows):
        line = ""
        for x in range(COLS):
            val = img_resized.getpixel((x, y))
            line += RAMP[int(val / 255 * n)]
        lines.append(line.rstrip())

    Path(__file__).parent.joinpath("portrait.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote portrait.txt ({COLS} cols x {rows} rows)")

if __name__ == "__main__":
    main()
