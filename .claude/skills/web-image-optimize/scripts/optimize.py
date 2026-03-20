#!/usr/bin/env python3
"""Optimize images for web usage.

Resizes, compresses, and converts source images to web-ready formats based
on a JSON spec file. Each image entry defines target dimensions, format,
quality, and fit mode.

Usage:
  python3 optimize.py --spec SPEC_FILE [--source DIR] [--output DIR] [--quality N] [FILE...]

The spec file is a JSON object mapping image basenames to their specs:
  {
    "image-name": {
      "width": 1920,
      "height": 1080,
      "format": "WEBP",    // WEBP, JPEG, or PNG
      "quality": 85,       // null for lossless PNG
      "fit": "cover"       // "cover" (resize+crop) or "contain" (fit within)
    }
  }
"""

import argparse
import json
from pathlib import Path

from PIL import Image

FORMAT_EXT = {"WEBP": ".webp", "JPEG": ".jpg", "PNG": ".png"}


def resize_cover(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Resize to cover target dimensions, then center-crop."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    new_w, new_h = round(iw * scale), round(ih * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - tw) // 2
    top = (new_h - th) // 2
    return img.crop((left, top, left + tw, top + th))


def resize_contain(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Resize to fit within target dimensions, preserving aspect ratio."""
    img.thumbnail((tw, th), Image.LANCZOS)
    return img


def optimize_image(src: Path, out_dir: Path, name: str, spec: dict) -> Path:
    tw, th = spec["width"], spec["height"]
    fmt = spec["format"]
    quality = spec.get("quality")
    fit = spec.get("fit", "cover")

    img = Image.open(src)

    if fmt == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    elif fmt == "PNG" and img.mode != "RGBA":
        img = img.convert("RGBA")

    if fit == "cover":
        img = resize_cover(img, tw, th)
    elif fit == "contain":
        img = resize_contain(img, tw, th)

    ext = FORMAT_EXT[fmt]
    out_path = out_dir / f"{name}{ext}"

    save_kwargs = {"format": fmt}
    if quality is not None:
        save_kwargs["quality"] = quality
    if fmt == "WEBP":
        save_kwargs["method"] = 6
    if fmt == "PNG":
        save_kwargs["optimize"] = True

    img.save(out_path, **save_kwargs)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Optimize images for web usage")
    parser.add_argument("--spec", required=True,
                        help="Path to JSON spec file defining image targets")
    parser.add_argument("--source", default=".",
                        help="Source directory containing input images (default: .)")
    parser.add_argument("--output", default="./web",
                        help="Output directory for optimized images (default: ./web)")
    parser.add_argument("--quality", type=int,
                        help="Override quality for lossy formats (1-100)")
    parser.add_argument("files", nargs="*",
                        help="Specific image basenames to process (without extension)")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    specs = json.loads(spec_path.read_text())

    src_dir = Path(args.source)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.files:
        names = [f for f in args.files if f in specs]
        unknown = [f for f in args.files if f not in specs]
        if unknown:
            print(f"Warning: unknown image names ignored: {', '.join(unknown)}")
            print(f"Known names: {', '.join(specs.keys())}")
    else:
        names = list(specs.keys())

    for name in names:
        src = src_dir / f"{name}.png"
        if not src.exists():
            print(f"SKIP {name}: {src} not found")
            continue

        spec = dict(specs[name])
        if args.quality is not None and spec.get("quality") is not None:
            spec["quality"] = args.quality

        out_path = optimize_image(src, out_dir, name, spec)
        src_size = src.stat().st_size / 1024
        out_size = out_path.stat().st_size / 1024
        ratio = (1 - out_size / src_size) * 100
        print(f"  {name}: {src_size:.0f}KB -> {out_size:.0f}KB ({ratio:.0f}% smaller) -> {out_path}")

    print("Done.")


if __name__ == "__main__":
    main()
