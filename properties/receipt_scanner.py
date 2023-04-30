import pytesseract
import cv2
from PIL import Image
import numpy as np
import re
from datetime import datetime

def preprocess_image(image_file):
    image = Image.open(image_file)
    image = image.resize((image.width * 3, image.height * 3), Image.BICUBIC)

    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 10, 7, 21)
    blurred_image = cv2.GaussianBlur(denoised_image, (5, 5), 0)

    adaptive_thresh = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    dilated_image = cv2.dilate(adaptive_thresh, kernel, iterations=1)

    return dilated_image

def extract_text(image):
    custom_config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(image, config=custom_config))
    return pytesseract.image_to_string(image, config=custom_config)

def extract_information(text):

    date_regex = r'\b\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}\b'
    date_match = re.search(date_regex, text)
    date = date_match.group(0) if date_match else None

    if date:
        try:
            parsed_date = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            try:
                parsed_date = datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                try:
                    parsed_date = datetime.strptime(date, '%d/%m/%y')
                except ValueError:
                    parsed_date = datetime.strptime(date, '%d.%m.%y')

        date = parsed_date.strftime('%Y-%m-%d')

    units_regex = r'\b(?:units|meter size|total units consumed)[^\d]*?(\d+)\b'
    units_match = re.search(units_regex, text, re.IGNORECASE)
    units = units_match.group(1) if units_match else None

    amount_regex = r'\b(?:total amount due)[:\s]*?[^\d]*(\d+(?:\.\d{2})?)\b'
    amount_match = re.search(amount_regex, text, re.IGNORECASE)
    amount = amount_match.group(1) if amount_match else None

    information = {
        'date': date,
        'amount': amount,
        'unit': units
    }
    return information

