"""
Image Handler Utilities

Functions for loading and processing images for PowerPoint insertion.
Handles file reading, dimension calculation, and aspect-ratio fitting.

Usage:
    from image_handler import load_image, image_exists, fit_dimensions
"""

import os
import warnings
from PIL import Image


def image_exists(file_path: str) -> bool:
    """Check if an image file exists and is accessible."""
    return os.path.isfile(file_path)


def get_image_dimensions(file_path: str) -> tuple[int, int]:
    """
    Get image dimensions in pixels.

    Returns:
        (width, height) tuple
    """
    with Image.open(file_path) as img:
        return img.size


def fit_dimensions(orig_width: float, orig_height: float,
                   max_width: float, max_height: float) -> tuple[float, float]:
    """
    Calculate dimensions to fit within bounds while preserving aspect ratio.

    Args:
        orig_width: original width (any unit, e.g. pixels)
        orig_height: original height (same unit)
        max_width: maximum target width (in inches for slides)
        max_height: maximum target height (in inches for slides)

    Returns:
        (width, height) tuple in target units
    """
    aspect = orig_width / orig_height
    width = max_width
    height = width / aspect
    if height > max_height:
        height = max_height
        width = height * aspect
    return (width, height)


def cover_dimensions(orig_width: float, orig_height: float,
                     target_width: float, target_height: float) -> tuple[float, float]:
    """
    Calculate dimensions to cover bounds (may crop) while preserving aspect ratio.
    """
    aspect = orig_width / orig_height
    target_aspect = target_width / target_height
    if aspect > target_aspect:
        height = target_height
        width = height * aspect
    else:
        width = target_width
        height = width / aspect
    return (width, height)


def center_position(image_width: float, image_height: float,
                    slide_width: float = 13.333,
                    slide_height: float = 7.5) -> tuple[float, float]:
    """
    Calculate x, y position to center an image on a slide.

    Returns:
        (x, y) tuple in inches
    """
    return (
        (slide_width - image_width) / 2,
        (slide_height - image_height) / 2,
    )


def load_images_from_directory(dir_path: str,
                               extensions: list[str] = None) -> list[dict]:
    """
    Load metadata for all images in a directory.

    Args:
        dir_path: path to directory
        extensions: allowed extensions (default: ['.png', '.jpg', '.jpeg'])

    Returns:
        list of dicts with keys: filename, path, width, height
    """
    if extensions is None:
        extensions = [".png", ".jpg", ".jpeg"]

    results = []
    if not os.path.isdir(dir_path):
        return results

    for fname in sorted(os.listdir(dir_path)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in extensions:
            full_path = os.path.join(dir_path, fname)
            try:
                w, h = get_image_dimensions(full_path)
                results.append({
                    "filename": fname,
                    "path": full_path,
                    "width": w,
                    "height": h,
                })
            except Exception as e:
                warnings.warn(f"Skipping unreadable image '{fname}': {e}")

    return results


def add_fitted_image(slide, image_path: str,
                     x: float, y: float,
                     max_width: float, max_height: float):
    """
    Add an image to a slide, automatically fitting it within the given bounds.

    Args:
        slide: pptx slide object
        image_path: path to image file
        x, y: top-left position in inches
        max_width, max_height: bounding box in inches
    """
    from pptx.util import Inches

    if not os.path.isfile(image_path):
        return None

    orig_w, orig_h = get_image_dimensions(image_path)
    fit_w, fit_h = fit_dimensions(orig_w, orig_h, max_width, max_height)

    # Center within the bounding box
    offset_x = x + (max_width - fit_w) / 2
    offset_y = y + (max_height - fit_h) / 2

    return slide.shapes.add_picture(
        image_path,
        Inches(offset_x), Inches(offset_y),
        Inches(fit_w), Inches(fit_h)
    )
