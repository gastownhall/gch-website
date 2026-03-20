---
name: remove-background
description: Remove the background from an image and make it transparent. Use when the user asks to remove a background, make an image transparent, isolate a subject, or prepare an image for compositing. Uses the rembg library with the u2net model.
---

# Remove Background

Remove backgrounds from images and output PNGs with transparent alpha channels. Uses the `rembg` library (u2net model) for AI-powered subject detection.

## Usage

Run the script with the project venv:

```bash
tmp/imgtools-venv/bin/python3 .claude/skills/remove-background/scripts/remove_background.py <input> [<output>]
```

- If `<output>` is omitted, appends `-nobg` to the filename (e.g., `logo.png` → `logo-nobg.png`).
- Output is always PNG (required for transparency).
- First run downloads the u2net model (~176MB) to `~/.u2net/`.

## Best Results

Works best on images with clear subject/background contrast — photos of people, objects, logos on solid backgrounds. May struggle with:
- Subjects that blend into the background color
- Complex scenes without a clear focal subject
- Dark subjects on dark backgrounds

## Dependencies

Requires the `imgtools-venv` virtual environment in `tmp/`. If missing, create it:

```bash
python3 -m venv tmp/imgtools-venv
tmp/imgtools-venv/bin/pip install rembg Pillow onnxruntime
```
