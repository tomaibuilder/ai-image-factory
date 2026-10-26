#!/usr/bin/env python3
"""
contact_sheet.py: numbered grid of draft images so you can pick by number.

Usage:
  python scripts/contact_sheet.py --out <folder>/contact-sheet.png <img1> <img2> ...
Numbers follow the order given. Prints the number-to-file map.
"""
import argparse, math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("images", nargs="+")
a = ap.parse_args()

TW, P = 640, 16  # thumbnail width, padding
ims = [Image.open(p).convert("RGB") for p in a.images]
th = round(TW * ims[0].height / ims[0].width)
cols = min(a.cols, len(ims))
rows = math.ceil(len(ims) / cols)
sheet = Image.new("RGB", (P + cols * (TW + P), P + rows * (th + P)), "#111")
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
except OSError:
    font = ImageFont.load_default()
for i, im in enumerate(ims):
    x, y = P + (i % cols) * (TW + P), P + (i // cols) * (th + P)
    sheet.paste(ImageOps.fit(im, (TW, th)), (x, y))  # mixed sizes crop, never stretch
    draw.rectangle((x, y, x + 72, y + 60), fill="#111")
    draw.text((x + 14, y + 6), str(i + 1), fill="#FFFFFF", font=font)
    print(f"{i + 1}: {a.images[i]}")
pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
sheet.save(a.out)
print(f"saved {a.out}")
