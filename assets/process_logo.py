"""
Logo processor for Kneeds.Knows.

Usage
-----
1. Save your original logo as `assets/logo-source.png` (or .jpg) in this folder.
2. Run:  python process_logo.py

It produces, in this same folder:
- logo.png       Cleaned full logo on solid white, trimmed, max-width 800
- logo-mark.png  Square crop of just the "K" symbol (1024x1024)
- favicon.png    32x32 favicon
- favicon-180.png  180x180 apple-touch-icon

What "cleaned up" means here:
- Forces near-white pixels (>=240,240,240) to pure #FFFFFF so the background is
  perfectly solid (kills JPEG fuzz around the logo).
- Trims uniform white margins to the actual artwork bounds.
- Re-pads with a clean 6% margin so the logo doesn't touch its edges.
- Re-saves as PNG with no compression artifacts.

Requirements:  pip install Pillow
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SOURCE_CANDIDATES = ["logo-source.png", "logo-source.jpg", "logo-source.jpeg"]

# Tuning knobs
WHITE_THRESHOLD = 240        # any RGB component >= this gets snapped to 255
PAD_PCT = 0.06               # 6% padding around trimmed artwork
TARGET_FULL_WIDTH = 800      # output width for logo.png
MARK_SIZE = 1024             # logo-mark.png is MARK_SIZE x MARK_SIZE


def find_source() -> Path:
    for name in SOURCE_CANDIDATES:
        p = HERE / name
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Drop your logo into {HERE} as one of: "
        + ", ".join(SOURCE_CANDIDATES)
    )


def snap_to_white(img: Image.Image) -> Image.Image:
    """Force near-white pixels to pure white so the background is solid."""
    img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD:
                pixels[x, y] = (255, 255, 255)
    return img


def trim_white(img: Image.Image) -> Image.Image:
    """Crop uniform white borders, then add a small even pad back."""
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = _difference(img, bg)
    bbox = diff.getbbox()
    if not bbox:
        return img
    cropped = img.crop(bbox)
    pad = int(max(cropped.size) * PAD_PCT)
    padded = Image.new("RGB", (cropped.width + 2 * pad, cropped.height + 2 * pad), (255, 255, 255))
    padded.paste(cropped, (pad, pad))
    return padded


def _difference(a: Image.Image, b: Image.Image) -> Image.Image:
    from PIL import ImageChops
    return ImageChops.difference(a.convert("RGB"), b.convert("RGB"))


def fit_width(img: Image.Image, target_width: int) -> Image.Image:
    if img.width <= target_width:
        return img
    ratio = target_width / img.width
    new_size = (target_width, round(img.height * ratio))
    return img.resize(new_size, Image.LANCZOS)


# Regions (as fractions of the image: left, top, right, bottom) to paint white
# before processing — kills stray scan artifacts above/around the artwork.
# Default targets the small smudge in the top-left of this logo.
CLEAN_BOXES = [
    (0.00, 0.00, 0.22, 0.13),   # top-left corner smudge
]

# Bounding box (fractions) of just the "K" symbol within the trimmed logo,
# excluding the "Kneeds.Knows" wordmark below it. Tweak if your crop is off.
MARK_BOX = (0.28, 0.06, 0.74, 0.77)


def whiten_boxes(img: Image.Image, boxes) -> Image.Image:
    """Paint the given fractional regions pure white (artifact removal)."""
    img = img.convert("RGB")
    w, h = img.size
    px = img.load()
    for (l, t, r, b) in boxes:
        x0, y0 = int(w * l), int(h * t)
        x1, y1 = int(w * r), int(h * b)
        for y in range(y0, y1):
            for x in range(x0, x1):
                px[x, y] = (255, 255, 255)
    return img


def extract_mark(img: Image.Image) -> Image.Image:
    """
    Crop just the K symbol using MARK_BOX, trim, and square-pad so it works
    as a favicon / app icon. Adjust MARK_BOX if the crop clips the symbol.
    """
    w, h = img.size
    l, t, r, b = MARK_BOX
    crop = img.crop((int(w * l), int(h * t), int(w * r), int(h * b)))
    crop = trim_white(crop)
    side = max(crop.size)
    square = Image.new("RGB", (side, side), (255, 255, 255))
    square.paste(crop, ((side - crop.width) // 2, (side - crop.height) // 2))
    return square


def main() -> None:
    src = find_source()
    print(f"Source: {src.name}")

    raw = Image.open(src)
    clean = snap_to_white(raw)
    clean = whiten_boxes(clean, CLEAN_BOXES)
    trimmed = trim_white(clean)

    full = fit_width(trimmed, TARGET_FULL_WIDTH)
    full.save(HERE / "logo.png", "PNG", optimize=True)
    print(f"  wrote logo.png       ({full.size[0]}x{full.size[1]})")

    mark = extract_mark(trimmed).resize((MARK_SIZE, MARK_SIZE), Image.LANCZOS)
    mark.save(HERE / "logo-mark.png", "PNG", optimize=True)
    print(f"  wrote logo-mark.png  ({MARK_SIZE}x{MARK_SIZE})")

    favicon = mark.resize((32, 32), Image.LANCZOS)
    favicon.save(HERE / "favicon.png", "PNG", optimize=True)
    print("  wrote favicon.png    (32x32)")

    apple = mark.resize((180, 180), Image.LANCZOS)
    apple.save(HERE / "favicon-180.png", "PNG", optimize=True)
    print("  wrote favicon-180.png (180x180)")

    print("\nDone. Reload the site to see the new logo.")


if __name__ == "__main__":
    main()
