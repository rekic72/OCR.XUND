#this function will be used for the interface
#suppsed to be inserted in main.py
def process_file(file_path):
    if file_path.endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        extracted_text = extract_text_from_image(file_path)
    else:
        raise Exception("Unsupported file format")

    word_counts.update(count_words(extracted_text))
    insert_into_db(os.path.basename(file_path), extracted_text)

    # Print the results (modify as needed)
    for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 1:
            print(f"{word}: {count}")