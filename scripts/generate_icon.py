#!/usr/bin/env python3
"""
GENERATE WINDOWS APP ICON (.ICO)
Uses Pillow to create a multi-resolution Windows Icon with tech shield and AI core.
Resolutions: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw

def create_icon_image(size):
    # Create high-res RGBA canvas
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(size * 0.06)
    w = size - 2 * pad
    h = size - 2 * pad

    # 1. Outer Dark Rounded Hexagon / Rounded Rect Background
    # Dark Navy gradient-like feel
    bg_color = (15, 23, 42, 255) # #0f172a
    radius = int(size * 0.22)
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        fill=bg_color,
        outline=(56, 189, 248, 255), # Cyan border
        width=max(1, int(size * 0.04))
    )

    # 2. Tech Shield Shape in center
    cx, cy = size / 2, size / 2
    sw = size * 0.38
    sh = size * 0.44

    # Shield polygon
    shield_pts = [
        (cx - sw, cy - sh * 0.7),
        (cx + sw, cy - sh * 0.7),
        (cx + sw, cy + sh * 0.1),
        (cx, cy + sh),
        (cx - sw, cy + sh * 0.1),
    ]

    draw.polygon(shield_pts, fill=(30, 41, 59, 255), outline=(99, 102, 241, 255)) # Indigo border

    # 3. Inner Glowing Core / Diamond AI Star
    dw = sw * 0.55
    dh = sh * 0.55
    diamond_pts = [
        (cx, cy - dh),
        (cx + dw, cy),
        (cx, cy + dh),
        (cx - dw, cy)
    ]
    draw.polygon(diamond_pts, fill=(0, 245, 255, 255)) # Glowing Neon Cyan

    # 4. Center Pupil / Spark
    pw = dw * 0.4
    draw.ellipse([cx - pw, cy - pw, cx + pw, cy + pw], fill=(255, 255, 255, 255))

    return img

def main():
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / 'assets'
    assets_dir.mkdir(exist_ok=True)
    ico_path = assets_dir / 'app-icon.ico'

    sizes = [256, 128, 64, 48, 32, 16]
    images = [create_icon_image(s) for s in sizes]

    # Save multi-size icon
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )

    print(f"Generated multi-resolution icon at: {ico_path}")
    print(f"Icon sizes embedded: {sizes}")

if __name__ == '__main__':
    main()
