"""Draw the link preview card served as og:image.

    python scripts/build_og_image.py

LinkedIn, Slack and X all fetch og:image when a link is pasted. Without one the
card renders as a bare title, so this draws a 1200x630 card: name, the two-line
tagline, affiliation, the site address, and the profile photo.

Output: assets/img/og-card.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "assets", "img", "og-card.png")
PHOTO = os.path.join(SITE, "assets", "img", "prof_pic.jpg")

W, H = 1200, 630
BG = (255, 255, 255)
INK = (23, 26, 31)
MUTED = (110, 118, 128)
ACCENT = (47, 111, 78)          # the green used across the site

FONT_DIRS = [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu"]
CANDIDATES = {
    "bold": ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "regular": ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"],
}


def font(kind, size):
    for d in FONT_DIRS:
        for name in CANDIDATES[kind]:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 14, H], fill=ACCENT)          # accent spine

    x, y = 80, 150
    d.text((x, y), "Young Jin Yoo", font=font("bold", 76), fill=INK)
    y += 100
    d.text((x, y), "Membrane-based integrated photonics", font=font("regular", 34), fill=INK)
    y += 48
    d.text((x, y), "Multi-physics simulation-driven design-to-fab",
           font=font("regular", 34), fill=INK)
    y += 72
    d.text((x, y), "Research Laboratory of Electronics, MIT",
           font=font("regular", 29), fill=MUTED)

    d.text((x, H - 90), "yjinyoo.github.io", font=font("bold", 30), fill=ACCENT)

    if os.path.exists(PHOTO):
        size = 260   # leaves clearance between the tagline and the circle
        photo = Image.open(PHOTO).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        img.paste(photo, (W - size - 72, (H - size) // 2), mask)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"{OUT}  {W}x{H}, {os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
