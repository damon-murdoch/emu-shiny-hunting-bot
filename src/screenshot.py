import math
import time
import numpy as np
from PIL import Image, ImageGrab
from skimage.metrics import structural_similarity as ssim

from src.system import get_dpi_scaling_factor as gdpi

import os

# Output Directory
OUTDIR = "out"

# Wait Limit
# Increase as necessary, Groudon is ~160
WAIT_LIMIT = 200

# Allowed Colour Difference
COLOUR_THRESHOLD = 16


def crop_image(image, crop_w=0.8, crop_h=0.8):
    # Parse image width/height
    width, height = image.size

    # Calculate cropping margins
    crop_margin_w = (1 - crop_w) / 2 * width
    crop_margin_h = (1 - crop_h) / 2 * height

    # Crop the image to the center portion
    left = crop_margin_w
    top = crop_margin_h
    right = width - crop_margin_w
    bottom = height - crop_margin_h

    # Return the cropped image
    return image.crop((left, top, right, bottom))


def load_image_data(image_path, debug=False):
    # Load image from path
    image = Image.open(image_path)

    # Crop the image to scale
    image = crop_image(image, 0.8, 0.5)

    # Convert image to grayscale
    image = image.convert("L")

    # [Debug]
    if debug:
        # Save a copy of the cropped greyscale image for testing
        image.save(f"{image_path.replace('.png', '.copy.png')}")

    # Return as np array
    return np.array(image)


def compare_images(a, b, debug=False):
    # Generate full paths
    pa = os.path.join(OUTDIR, a)
    pb = os.path.join(OUTDIR, b)

    # Load both images
    fa = load_image_data(pa, debug=debug)
    fb = load_image_data(pb, debug=debug)

    # Compare the two images
    similarity, _ = ssim(fa, fb, full=True)

    return similarity


def take_screenshot(window):
    # Window scaling factor
    sf = gdpi()

    # Bounding Box

    bbox = [
        window.left * sf,  # Left
        window.top * sf,  # Top
        (window.left + window.width) * sf,  # Right
        (window.top + window.height) * sf,  # Bottom
    ]

    # Take a screenshot of the window and return it
    return ImageGrab.grab(bbox=bbox, all_screens=True)


def save_screenshot(window, name="screenshot.png", format="PNG"):
    # Take a screenshot of the window
    image = take_screenshot(window)

    # Create the output directory
    os.makedirs(OUTDIR, exist_ok=True)

    # Create the output filename
    filename = os.path.join(OUTDIR, name)

    # Save the screenshot
    image.save(filename, format)


def wait_for_change(
    window, x=None, y=None, delay=0.1, limit=WAIT_LIMIT, threshold=COLOUR_THRESHOLD
):
    # X Coordinate not provided
    if x == None:
        # Center Pixel
        x = math.floor(window.width / 2)

    # Y Coordinate not provided
    if y == None:
        # Center Pixel (Bottom Screen)
        y = math.floor((window.height * 2) / 3)

    # Pixel tuple
    point = (x, y)

    screenshot = take_screenshot(window)
    first = screenshot.getpixel(point)
    pixel = first

    i = 0

    # Wait for change
    while in_colour_threshold(pixel, first, threshold):
        # Limit exceeded
        if i > limit:
            raise Exception(f"Wait for change limit '{limit}' exceeded!")

        screenshot = take_screenshot(window)
        pixel = screenshot.getpixel(point)

        time.sleep(delay)

        i += 1

    # Colour changed
    return i


def check_for_colour(window, x=None, y=None, r=0, g=0, b=0, threshold=COLOUR_THRESHOLD):
    # X Coordinate not provided
    if x == None:
        # Center Pixel
        x = math.floor(window.width / 2)

    # Y Coordinate not provided
    if y == None:
        # Center Pixel (Bottom Screen)
        y = math.floor((window.height * 2) / 3)

    # Pixel tuple
    point = (x, y)

    # Target colour
    target = (r, g, b)

    screenshot = take_screenshot(window)
    pixel = screenshot.getpixel(point)

    # True/False if matches
    return in_colour_threshold(pixel, target, threshold)


# New helper function to check if the color is within a given threshold
def in_colour_threshold(pixel, target, threshold=16):
    if None in pixel:
        return False
    if None in target:
        raise Exception("'None' in target pixel!")

    # Dereference RGB values
    r1, g1, b1 = pixel
    r2, g2, b2 = target

    # Calculate differences
    dr = abs(r1 - r2)
    dg = abs(g1 - g2)
    db = abs(b1 - b2)

    # Total difference is less than 'threshold'
    return (dr + dg + db) < threshold


def wait_for_colour(
    window,
    x=None,
    y=None,
    r=0,
    g=0,
    b=0,
    delay=0.1,
    limit=WAIT_LIMIT,
    threshold=COLOUR_THRESHOLD,
):
    # X Coordinate not provided
    if x == None:
        # Center Pixel
        x = math.floor(window.width / 2)

    # Y Coordinate not provided
    if y == None:
        # Center Pixel (Bottom Screen)
        y = math.floor((window.height * 2) / 3)

    # Pixel tuple
    point = (x, y)

    # Target colour
    target = (r, g, b)

    # Placeholder pixel
    pixel = (None, None, None)

    i = 0

    # While the correct colour has not been found
    while not in_colour_threshold(pixel, target, threshold):
        # Limit exceeded
        if i > limit:
            raise Exception(f"Wait for colour limit '{limit}' exceeded!")

        screenshot = take_screenshot(window)
        pixel = screenshot.getpixel(point)

        time.sleep(delay)

        i += 1

    # Desired colour found
    return i
