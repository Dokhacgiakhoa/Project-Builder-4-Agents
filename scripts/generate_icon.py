import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

def generate_custom_app_icon():
    root = Path(r'D:/Github/Project-Starter-Kit')
    assets_dir = root / 'assets'
    logo_mark_path = assets_dir / 'logo-mark.png'
    ico_output_path = assets_dir / 'app-icon.ico'

    if not logo_mark_path.exists():
        print("logo-mark.png not found")
        return

    logo_img = Image.open(logo_mark_path).convert('RGBA')

    sizes = [256, 128, 64, 48, 32, 16]
    icon_layers = []

    for s in sizes:
        # Create base canvas with transparency
        canvas = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        pad = max(1, int(s * 0.05))
        corner_r = int(s * 0.22)

        # 1. Dark squircle background (#0b0f19 with subtle border)
        bg_rect = [pad, pad, s - pad, s - pad]
        draw.rounded_rectangle(
            bg_rect,
            radius=corner_r,
            fill=(11, 15, 25, 255),
            outline=(16, 185, 129, 180), # Emerald green subtle border
            width=max(1, int(s * 0.035))
        )

        # 2. Fit the logo-mark inside the squircle
        logo_area = int(s * 0.65)
        # Calculate aspect ratio
        orig_w, orig_h = logo_img.size
        ratio = min(logo_area / orig_w, logo_area / orig_h)
        target_w = int(orig_w * ratio)
        target_h = int(orig_h * ratio)

        resized_logo = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Center position
        pos_x = (s - target_w) // 2
        pos_y = (s - target_h) // 2

        canvas.alpha_composite(resized_logo, (pos_x, pos_y))
        icon_layers.append(canvas)

    # Save to ICO
    icon_layers[0].save(
        ico_output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=icon_layers[1:]
    )
    print(f"Successfully generated app-icon.ico with custom 'P' logo at {ico_output_path}")

    # Also save a 256x256 preview PNG for web/docs
    icon_layers[0].save(assets_dir / 'app-icon-preview.png')
    print("Saved preview to assets/app-icon-preview.png")

if __name__ == '__main__':
    generate_custom_app_icon()
