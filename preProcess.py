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

            text += pytesseract.image_to_string(thresh_img)

        return text
