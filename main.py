import configparser
import os
import sqlite3

import cv2
import fitz
import mysql.connector
import numpy as np
import pytesseract
import pandas as pd

# raed configuration file in config folder
config = configparser.ConfigParser()
config.read("config/config.ini")

pytesseract.pytesseract.tesseract_cmd = config.get("DEFAULT", "tesseract_path")

# connect to database
mydb = mysql.connector.connect(
    host=config.get("database", "host"),
    user=config.get("database", "user"),
    password=config.get("database", "password"),
    database=config.get("database", "database")
)

# create a cursor object to execute the import of a new pdf file and store it into the database
# is an object provided by MySQL connector library, allows the communication with database
mycursor = mydb.cursor()

# create a table if it not exists yet with the name pdf_text
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS pdf_text (id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255), text LONGTEXT)")


# develop a function that extract text from pdf using ocr
# first open pdf file and assign it to object pdfFileObj
# we will initialize an empty string used to store the extracted text from pdf by using text = ""
def extract_text_from_pdf(filename):
    with fitz.open(filename) as doc:
        text = ""
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)

            # Preprocessing
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            _, thresh_img = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # here we got to retrieve the german language package from pytesseract stored locally on a C:drive
            text += pytesseract.image_to_string(thresh_img, lang='deu')

        return text


# function to insert the text from the pdf file into the database
# we are creating a query to insert value filename and text into the pdf_text table
def insert_into_db(filename, text):
    sql = "INSERT INTO pdf_text (filename, text) VALUES (%s, %s)"
    val = (filename, text)
    mycursor.execute(sql, val)
    mydb.commit()


import collections


def count_words(text):
    words = text.lower().split()
    return collections.Counter(words)


word_counts = collections.Counter()

# go through all pdfs within one directory, extract text from each pdf using ocr functionalities
# store text data in the database
folder_path = 'C:\\Users\\rekic\\OneDrive\\Dokumente\\FHWN\\2. Sem\\HC Project 1\\scanFiles'

for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)  # used to construct the full path to an file

        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            continue

        word_counts.update(count_words(extracted_text))

        print(f"Extracted text from {filename}:\n")
        print(extracted_text)
        print("\n" + "-" * 80 + "\n")  # Print a separator line between files
        insert_into_db(filename, extracted_text)
    except Exception as e:
        print(f"Error processing {filename}: {e}")

for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
    if count > 1:
        print(f"{word}: {count}")

# close the database connection
# mydb.close()


for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)

        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            continue

        word_counts.update(count_words(extracted_text))

        insert_into_db(filename, extracted_text)
    except Exception as e:
        print(f"Error processing {filename}: {e}")


def process_file(file_path):
    if file_path.endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        raise Exception("Unsupported file format")

    word_counts.update(count_words(extracted_text))
    insert_into_db(os.path.basename(file_path), extracted_text)


    # Print the results (modify as needed)
    for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 1:
            print(f"{word}: {count}")
