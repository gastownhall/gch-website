#!/usr/bin/env python3
"""Remove background from an image, making it transparent.

Usage: remove_background.py <input> [<output>]

If output is omitted, appends '-nobg' before the extension.
Output is always PNG (transparency requires alpha channel).
"""

import sys
import os
from rembg import remove
from PIL import Image


def remove_bg(input_path, output_path):
    """Remove background from input image and save with transparency."""
    img = Image.open(input_path)
    result = remove(img)
    result.save(output_path, "PNG")
    print(f"Background removed: {output_path}")


def default_output_path(input_path):
    """Generate output path by appending '-nobg'."""
    base, _ = os.path.splitext(input_path)
    return base + "-nobg.png"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output_path(input_path)

    remove_bg(input_path, output_path)
