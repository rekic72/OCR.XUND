import tkinter as tk
from tkinter import filedialog
import sqlite3
from main import process_file

# connect sqlitedb and create Database
conn = sqlite3.connect("testdb3.db")
mycursor = conn.cursor()

mycursor.execute(''' 
            CREATE TABLE IF NOT EXISTS pdf_text 
            (word_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            text TEXT,
            count INT)    
            ''')


class OCRApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                df = process_file(file_path)

                # Save the DataFrame to an Excel file
                output_file = 'ExtractionOcr.xlsx'
                df.to_excel(output_file, index=False)

                ## -> insert df into sqlite
                data = df.to_records(index=False).tolist()
                mycursor.executemany("""INSERT INTO pdf_text(Text,Count) VALUES (?,?)""", data)
                conn.commit()

                self.result_label.config(
                    text=f"OCR text extraction successful. Results saved to {output_file}."
                )
            except Exception as e:
                self.result_label.config(text=f"Error processing the file: {e}")


# SELECT-Abfrage ausführen und Ergebnisse nach count absteigend sortieren
# Anzeige in PopUp
mycursor.execute("SELECT text, count FROM pdf_text ORDER BY count DESC")
rows = mycursor.fetchall()

# Ein neues Popup-Fenster erstellen
popup = tk.Tk()
popup.title("Datenbankabfrage")

# Eine Scrollbar hinzufügen
scrollbar = tk.Scrollbar(popup)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Ein neues Text-Widget im Popup-Fenster erstellen
text_widget = tk.Text(popup, yscrollcommand=scrollbar.set)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

# Datensätze als formatierten Text hinzufügen
for row in rows:
    text_widget.insert(tk.END, "Text: {}\n".format(row[0]))
    text_widget.insert(tk.END, "Count: {}\n\n".format(row[1]))

# Scrollbar mit dem Text-Widget verknüpfen
scrollbar.config(command=text_widget.yview)

# Popup-Fenster öffnen und auf Ereignisse warten
popup.mainloop()

conn.commit()
conn.close()
mycursor.close()


def main():
    root = tk.Tk()
    root.title("OCR Text Extraction")
    app = OCRApp(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
