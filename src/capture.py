# capture.py

try:
    from PIL import ImageGrab
except ImportError:
    raise ImportError("Please install Pillow: pip install pillow")

def capture_region(x, y, width, height):
    """
    Captures the specified screen region and returns it as a PIL.Image.
    """
    bbox = (x, y, x + width, y + height)
    return ImageGrab.grab(bbox)
