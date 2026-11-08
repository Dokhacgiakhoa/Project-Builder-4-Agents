import os
import sys
import re
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def build_brand_assets():
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("Usage: python scripts/build_brand_assets.py <path/to/clean_logo_mask.png>")
        return
    mask_path = Path(sys.argv[1])
    if not mask_path.exists():
        print(f"Error: {mask_path} not found")
        return

    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    h, w = mask.shape
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    comps = sorted(range(1, num_labels), key=lambda i: stats[i, cv2.CC_STAT_AREA], reverse=True)

    head_mask = (labels == comps[0]).astype(np.uint8) * 255
    stem_mask = (labels == comps[1]).astype(np.uint8) * 255

    # Upscale 8x for subpixel tracing
    scale_subpixel = 8
    head_8x = cv2.resize(head_mask, (w * scale_subpixel, h * scale_subpixel), interpolation=cv2.INTER_LANCZOS4)
    stem_8x = cv2.resize(stem_mask, (w * scale_subpixel, h * scale_subpixel), interpolation=cv2.INTER_LANCZOS4)

    _, head_th = cv2.threshold(head_8x, 127, 255, cv2.THRESH_BINARY)
    _, stem_th = cv2.threshold(stem_8x, 127, 255, cv2.THRESH_BINARY)

    cnt_h = cv2.findContours(head_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)[0][0]
    cnt_s = cv2.findContours(stem_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)[0][0]

    all_pts = np.vstack([cnt_h, cnt_s])
    bx, by, bw, bh = cv2.boundingRect(all_pts)

    # Standardize to 512x512 viewBox
    target_h = 360.0
    norm_scale = target_h / bh
    norm_w = bw * norm_scale
    offset_x = (512 - norm_w) / 2.0
    offset_y = (512 - target_h) / 2.0

    def contour_to_svg(cnt, eps=0.0016):
        arc = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, eps * arc, True)
        parts = []
        for i, pt in enumerate(approx):
            px = offset_x + (pt[0][0] - bx) * norm_scale
            py = offset_y + (pt[0][1] - by) * norm_scale
            cmd = "M" if i == 0 else "L"
            parts.append(f"{cmd} {px:.2f} {py:.2f}")
        parts.append("Z")
        return " ".join(parts), approx

    path_h_d, approx_h = contour_to_svg(cnt_h, 0.0015)
    path_s_d, approx_s = contour_to_svg(cnt_s, 0.0015)

    print(f"Generated Vector Geometry: Head {len(approx_h)} pts, Stem {len(approx_s)} pts")

    # 1. assets/logo-mark.svg
    logo_mark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="brandGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" />
      <stop offset="35%" stop-color="#14b8a6" />
      <stop offset="70%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
  </defs>
  <g fill="url(#brandGradient)">
    <!-- Outer P Loop / Head -->
    <path d="{path_h_d}" />
    <!-- Inner Upward Arrow / Stem -->
    <path d="{path_s_d}" />
  </g>
</svg>
'''
    (assets_dir / 'logo-mark.svg').write_text(logo_mark_svg, encoding='utf-8')
    print("Saved assets/logo-mark.svg")

    # 2. assets/logo.svg (Horizontal Lockup)
    logo_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 260" width="100%" height="100%">
  <defs>
    <linearGradient id="logoBrandGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" />
      <stop offset="35%" stop-color="#14b8a6" />
      <stop offset="70%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
  </defs>

  <!-- Vector Logo Mark on Left -->
  <g transform="translate(10, 0) scale(0.50)" fill="url(#logoBrandGrad)">
    <path d="{path_h_d}" />
    <path d="{path_s_d}" />
  </g>

  <!-- Brand Typography -->
  <g transform="translate(280, 120)">
    <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="52" font-weight="900" fill="#0f172a" letter-spacing="-1">
      PROJECT
    </text>
    <text x="240" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="52" font-weight="900" fill="url(#logoBrandGrad)" letter-spacing="-1">
      STARTER KIT
    </text>
    <text y="42" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="17" font-weight="600" fill="#64748b" letter-spacing="3.5">
      UNIVERSAL AI-NATIVE DELIVERY FRAMEWORK
    </text>
  </g>
</svg>
'''
    (assets_dir / 'logo.svg').write_text(logo_svg, encoding='utf-8')
    print("Saved assets/logo.svg")

    # 3. assets/logo-stacked.svg (Centered Lockup)
    logo_stacked_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 700" width="100%" height="100%">
  <defs>
    <linearGradient id="stackedGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" />
      <stop offset="35%" stop-color="#14b8a6" />
      <stop offset="70%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
  </defs>

  <!-- Centered Logo Mark -->
  <g transform="translate(44, 20) scale(1.0)" fill="url(#stackedGrad)">
    <path d="{path_h_d}" />
    <path d="{path_s_d}" />
  </g>

  <!-- Centered Typography -->
  <g transform="translate(300, 570)" text-anchor="middle">
    <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="44" font-weight="900" fill="#0f172a" letter-spacing="2">
      PROJECT <tspan fill="url(#stackedGrad)">STARTER KIT</tspan>
    </text>
    <text y="42" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="16" font-weight="600" fill="#64748b" letter-spacing="4">
      UNIVERSAL AI-NATIVE FRAMEWORK
    </text>
  </g>
</svg>
'''
    (assets_dir / 'logo-stacked.svg').write_text(logo_stacked_svg, encoding='utf-8')
    print("Saved assets/logo-stacked.svg")

    # 4. Render High-Resolution Antialiased Raster PNGs (1024x1024)
    canvas_size = 2048
    target_render_h = 1440.0
    r_scale = target_render_h / bh
    r_w = bw * r_scale
    r_off_x = (canvas_size - r_w) / 2.0
    r_off_y = (canvas_size - target_render_h) / 2.0

    poly_h = np.round((cnt_h.reshape(-1, 2) - [bx, by]) * r_scale + [r_off_x, r_off_y]).astype(np.int32)
    poly_s = np.round((cnt_s.reshape(-1, 2) - [bx, by]) * r_scale + [r_off_x, r_off_y]).astype(np.int32)

    alpha_canvas = np.zeros((canvas_size, canvas_size), dtype=np.uint8)
    cv2.fillPoly(alpha_canvas, [poly_h], 255)
    cv2.fillPoly(alpha_canvas, [poly_s], 255)

    # Downscale with Lanczos for smooth subpixel antialiasing
    alpha_1024 = Image.fromarray(alpha_canvas).resize((1024, 1024), Image.Resampling.LANCZOS)
    alpha_arr = np.array(alpha_1024)

    # Generate 1024x1024 diagonal color gradient
    x_grid = np.linspace(0, 1, 1024)
    y_grid = np.linspace(1, 0, 1024)
    xx, yy = np.meshgrid(x_grid, y_grid)
    t = (xx + yy) / 2.0

    r = np.interp(t, [0.0, 0.35, 0.70, 1.0], [6, 20, 16, 52])
    g = np.interp(t, [0.0, 0.35, 0.70, 1.0], [182, 184, 185, 211])
    b = np.interp(t, [0.0, 0.35, 0.70, 1.0], [212, 166, 129, 153])

    rgba_mark = np.dstack([r, g, b, alpha_arr]).astype(np.uint8)
    logo_mark_img = Image.fromarray(rgba_mark, 'RGBA')
    logo_mark_img.save(assets_dir / 'logo-mark.png')
    print("Saved assets/logo-mark.png (1024x1024 High-Res Antialiased)")

    # Also build full horizontal logo.png
    full_w, full_h = 1900, 520
    full_canvas = Image.new('RGBA', (full_w, full_h), (0, 0, 0, 0))
    # Place scaled logo mark
    mark_sized = logo_mark_img.resize((480, 480), Image.Resampling.LANCZOS)
    full_canvas.alpha_composite(mark_sized, (30, 20))

    # Draw typography
    draw = ImageDraw.Draw(full_canvas)
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 96)
        font_sub = ImageFont.truetype("arial.ttf", 36)
    except (OSError, IOError):
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((540, 120), "PROJECT ", fill=(15, 23, 42, 255), font=font_main)
    # Gradient text approximation for "STARTER KIT"
    draw.text((1010, 120), "STARTER KIT", fill=(16, 185, 129, 255), font=font_main)
    draw.text((545, 240), "UNIVERSAL AI-NATIVE DELIVERY FRAMEWORK", fill=(100, 116, 139, 255), font=font_sub)
    full_canvas.save(assets_dir / 'logo.png')
    print("Saved assets/logo.png (High-Res Horizontal Lockup)")

    # 5. Build Multi-Resolution app-icon.ico and app-icon-preview.png
    sizes = [256, 128, 64, 48, 32, 16]
    layers = []
    for s in sizes:
        canv = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(canv)

        pad = max(1, int(s * 0.05))
        corner_r = int(s * 0.22)
        bg_rect = [pad, pad, s - pad, s - pad]

        # Dark Squircle background
        d.rounded_rectangle(
            bg_rect,
            radius=corner_r,
            fill=(11, 15, 25, 255),
            outline=(16, 185, 129, 200),
            width=max(1, int(s * 0.035))
        )

        # Fit logo mark inside squircle
        logo_area = int(s * 0.65)
        res_mark = logo_mark_img.resize((logo_area, logo_area), Image.Resampling.LANCZOS)
        pos = (s - logo_area) // 2
        canv.alpha_composite(res_mark, (pos, pos))
        layers.append(canv)

    layers[0].save(
        assets_dir / 'app-icon.ico',
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=layers[1:]
    )
    print("Saved assets/app-icon.ico (256, 128, 64, 48, 32, 16)")

    layers[0].save(assets_dir / 'app-icon-preview.png')
    print("Saved assets/app-icon-preview.png")

    # 6. Update assets/banner.svg with true vector logo mark
    banner_path = assets_dir / 'banner.svg'
    if banner_path.exists():
        content = banner_path.read_text(encoding='utf-8')
        # Replace the base64 raster image block with the true vector geometry
        vector_banner_block = f'''  <!-- Brand Vector Logo Mark (P Monogram) -->
  <g transform="translate(565, 20) scale(0.14)" fill="url(#titleGrad)">
    <path d="{path_h_d}" />
    <path d="{path_s_d}" />
  </g>'''

        # Match image tag if present
        new_content = re.sub(
            r'<g transform="translate\(600,\s*50\)">\s*<image[^>]+>\s*</g>',
            vector_banner_block,
            content
        )
        banner_path.write_text(new_content, encoding='utf-8')
        print("Updated assets/banner.svg with pure vector logo mark")

if __name__ == '__main__':
    build_brand_assets()
