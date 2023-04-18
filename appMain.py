# this code is the fundament to the app.py which starts
# the application with the main()

import collections
import configparser
import os
import sqlite3
import tempfile

import pandas as pd
import pytesseract
from pdf2image import convert_from_path

config = configparser.ConfigParser()
config.read("config/config.ini")

pytesseract.pytesseract.tesseract_cmd = config.get("DEFAULT", "tesseract_path")


def extract_text_from_pdf(file_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to a list of images
        images = convert_from_path(file_path, output_folder=temp_dir)

        extracted_text = ""
        for img in images:
            # Extract text from image
            text = pytesseract.image_to_string(img, lang='deu')
            extracted_text += text + "\n"

    return extracted_text


def count_words(text):
    words = text.lower().split()
    return collections.Counter(words)


def process_file(file_path):
    if file_path.endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        raise Exception("Unsupported file format")

    word_counts = count_words(extracted_text)

    # Save word counts to a DataFrame and return it
    df = pd.DataFrame(word_counts.items(), columns=["Word", "Count"])
    return df

    # Print the results (modify as needed)
    print(f"Extracted text from {os.path.basename(file_path)}:\n")
    print(extracted_text)


if __name__ == "__main__":
    # Example usage (optional, for testing)
    process_file("path/to/your/test.pdf")
