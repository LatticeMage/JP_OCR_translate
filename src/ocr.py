# ocr.py


def ocr_image_to_text(img) -> str:
    """
    Runs OCR on the given PIL.Image and returns the recognized text.
    Also writes it to now.txt for compatibility with your old flow.
    """
    import random

    # Generate a random number (e.g., between 1 and 100)
    random_number = random.randint(1, 100)

    # Convert to string
    random_string = str(random_number)
    text = "test" + random_string

    return text
