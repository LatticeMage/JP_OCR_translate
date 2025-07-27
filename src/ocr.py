import easyocr
import numpy as np

# Initialize EasyOCR reader for Japanese (add other languages as needed)
reader = easyocr.Reader(['ja'], gpu=False)

def ocr_image_to_text(img) -> str:
    """
    Runs OCR on the given PIL.Image (or numpy array) and returns the recognized text.
    Also writes it to now.txt for compatibility with your old flow.
    """
    # Convert PIL.Image to NumPy array if needed
    if not isinstance(img, np.ndarray):
        img_array = np.array(img)
    else:
        img_array = img

    # Perform OCR (detail=0 returns plain text lines)
    results = reader.readtext(img_array, detail=0)

    # Combine lines into single text block
    text = "\n".join(results)

    return text
