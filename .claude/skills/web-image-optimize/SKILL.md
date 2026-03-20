---
name: web-image-optimize
description: Optimize images for web usage. Resizes, compresses, and converts source PNGs to web-ready formats (WebP, JPG, PNG) per a project-specific JSON spec. Use when adding or updating images for a website.
---

# Web Image Optimize

Compress and resize source images to web-optimized outputs using a JSON spec file that defines target dimensions, format, and quality per image.

## Usage

```bash
# Optimize all images defined in a spec file
python3 .claude/skills/web-image-optimize/scripts/optimize.py \
  --spec path/to/image-specs.json \
  --source path/to/source/images \
  --output path/to/output/web

# Optimize specific images only
python3 .claude/skills/web-image-optimize/scripts/optimize.py \
  --spec image-specs.json --source ./images --output ./images/web \
  background logo

# Override quality for lossy formats
python3 .claude/skills/web-image-optimize/scripts/optimize.py \
  --spec image-specs.json --source ./images --output ./images/web \
  --quality 92
```

## Spec File Format

The `--spec` file is JSON mapping image basenames to their target specs:

```json
{
  "hero-banner": {
    "width": 1920,
    "height": 1080,
    "format": "WEBP",
    "quality": 85,
    "fit": "cover"
  },
  "logo": {
    "width": 512,
    "height": 512,
    "format": "PNG",
    "quality": null,
    "fit": "contain"
  }
}
```

Fields:
- `width`, `height` — target pixel dimensions
- `format` — `"WEBP"`, `"JPEG"`, or `"PNG"`
- `quality` — integer (1-100) for lossy formats, `null` for lossless PNG
- `fit` — `"cover"` (resize + center-crop to fill) or `"contain"` (fit within bounds, preserve aspect ratio)

Source images are expected as `.png` files named `{basename}.png` in the source directory.

## Dependencies

Requires Pillow. If using an imgtools venv:
```bash
python3 -m venv tmp/imgtools-venv
tmp/imgtools-venv/bin/pip install Pillow
```
