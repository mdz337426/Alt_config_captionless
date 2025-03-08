from openpyxl import load_workbook
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import base64


def extract_alt_text_examples(file_path, num_examples=5):
    wb = load_workbook(file_path)
    sheet = wb.active  # Select the first sheet
    # Extract the first `num_examples` rows for context
    examples = []
    for i in range(num_examples):
        alt_text = sheet[f'G{i+3}'].value
        if alt_text:
            examples.append(f"{i+1}.\n{alt_text}")
    wb.close()
    return "\n\n".join(examples)

def crop_image(image):
    open_cv_image = np.array(image)

    # Convert to grayscale and apply threshold to find content
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find non-zero pixels (content area)
    coords = cv2.findNonZero(thresh)

    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped_image = open_cv_image[y:y+h, x:x+w]

        # Save cropped image
        cropped_pil = Image.fromarray(cropped_image)
        buffered = BytesIO()
        cropped_pil.save(buffered, format="PNG")  # You can use "JPEG" if needed
        base64_string = base64.b64encode(buffered.getvalue()).decode()
        return base64_string

