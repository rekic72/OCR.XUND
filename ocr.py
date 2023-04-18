#additionally

# Initialize a list to store the names of processed PDF files
processed_files = []

folder_path = 'C:\\Users\\rekic\\OneDrive\\Dokumente\\FHWN\\2. Sem\\HC Project 1\\pdffiles'

for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        try:
            file_path = os.path.join(folder_path, filename)
            pdf_text = extract_text_from_pdf(file_path)
            print(f"Extracted text from {filename}:\n")
            print(pdf_text)  # This line will print the extracted text to the console
            print("\n" + "-" * 80 + "\n")  # Print a separator line between files
            insert_into_db(filename, pdf_text)

            # Add the filename to the processed_files list
            processed_files.append(filename)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Print the number of processed PDF files and their names
print(f"Number of processed PDF files: {len(processed_files)}")
print("Processed PDF files:")
for file in processed_files:
    print(file)
