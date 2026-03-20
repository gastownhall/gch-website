#!/usr/bin/env python3
"""Remove the 4-pointed star watermark from the bottom-right corner of images.

Usage: remove_watermark.py <input> [<output>]

If output is omitted, writes to the same filename without the '-wm' suffix,
or appends '-clean' before the extension.
"""

import sys
import os
import numpy as np
import cv2


def find_watermark_mask(img, region_size=200, threshold=120):
    """Detect the star watermark in the bottom-right corner and return a mask."""
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Extract bottom-right corner
    corner = gray[h - region_size:, w - region_size:]

    # Threshold to find bright watermark pixels against dark background
    _, binary = cv2.threshold(corner, threshold, 255, cv2.THRESH_BINARY)

    # Dilate to ensure full coverage for inpainting
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    dilated = cv2.dilate(binary, kernel, iterations=2)

    # Build full-image mask
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[h - region_size:, w - region_size:] = dilated

    return mask


def remove_watermark(input_path, output_path):
    """Remove watermark from input image and save to output path."""
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image: {input_path}", file=sys.stderr)
        sys.exit(1)

    mask = find_watermark_mask(img)

    # Check if watermark was actually found
    if cv2.countNonZero(mask) == 0:
        print(f"No watermark detected in {input_path}")
        cv2.imwrite(output_path, img)
        return

    # Inpaint the watermark region
    result = cv2.inpaint(img, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    cv2.imwrite(output_path, result)
    print(f"Watermark removed: {output_path}")


def default_output_path(input_path):
    """Generate output path by removing '-wm' or appending '-clean'."""
    base, ext = os.path.splitext(input_path)
    if base.endswith("-wm"):
        return base[:-3] + ext
    return base + "-clean" + ext


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output_path(input_path)

    remove_watermark(input_path, output_path)
