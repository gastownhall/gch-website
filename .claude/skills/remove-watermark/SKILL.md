---
name: remove-watermark
description: Remove the 4-pointed star AI-generator watermark from the bottom-right corner of PNG images. Use when the user asks to remove watermarks, clean up generated images, or prepare marketing images for production use.
---

# Remove Watermark

Remove the small 4-pointed star watermark that AI image generators place in the bottom-right corner of images. Uses OpenCV inpainting to seamlessly fill the watermark region.

## Usage

Run the script with the project venv:

```bash
tmp/imgtools-venv/bin/python3 .claude/skills/remove-watermark/scripts/remove_watermark.py <input> [<output>]
```

- If `<output>` is omitted, strips `-wm` from the filename (e.g., `foo-wm.png` → `foo.png`) or appends `-clean`.
- Works on any PNG with the standard bottom-right star watermark.

## Batch Processing

To process all watermarked images in a directory:

```bash
for f in /path/to/images/*-wm.png; do
  tmp/imgtools-venv/bin/python3 .claude/skills/remove-watermark/scripts/remove_watermark.py "$f"
done
```

## Dependencies

Requires the `imgtools-venv` virtual environment in `tmp/`. If missing, create it:

```bash
python3 -m venv tmp/imgtools-venv
tmp/imgtools-venv/bin/pip install opencv-python-headless Pillow
```
