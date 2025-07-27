try:
    from PIL import ImageGrab
except ImportError:
    raise ImportError("Please install Pillow: pip install pillow")


def capture_region(x, y, width, height, output_path="now.png"):
    """
    Captures the specified screen region and saves it as an image.

    Parameters:
        x (int): X-coordinate of the top-left corner.
        y (int): Y-coordinate of the top-left corner.
        width (int): Width of the region.
        height (int): Height of the region.
        output_path (str): Path to save the image.
    """
    # Define bounding box (left, top, right, bottom)
    bbox = (x, y, x + width, y + height)
    # Capture the screen region
    img = ImageGrab.grab(bbox)
    # Save the image
    img.save(output_path)
