#additionally jpegs shall be processed too

def extract_text_from_image(filename):
    img = cv2.imread(filename)

    # Preprocessing
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    _, thresh_img = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(thresh_img)
    return text

# ... (previous functions and setup)

folder_path = 'C:\\Users\\rekic\\OneDrive\\Dokumente\\FHWN\\2. Sem\\HC Project 1\\pdffiles'

for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)

        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.jpg'):
            extracted_text = extract_text_from_image(file_path)
        else:
            continue

        print(f"Extracted text from {filename}:\n")
        print(extracted_text)  # This line will print the extracted text to the console
        print("\n" + "-" * 80 + "\n")  # Print a separator line between files
        insert_into_db(filename, extracted_text)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
