import tkinter as tk
from tkinter import filedialog
from pdf2docx import Converter
import os


def select_pdf_file_and_convert():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # Extract the filename without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Set the output DOCX path in the "Downloads" directory
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        output_docx = os.path.join(downloads_dir, file_name + ".docx")

        pdf_to_docx(file_path, output_docx)

def pdf_to_docx(input_pdf, output_docx):
    cv = Converter(input_pdf)
    cv.convert(output_docx, start=0, end=None)
    
    # Open the converted DOCX file and set the font to Arial Unicode MS
    from docx import Document
    doc = Document(output_docx)
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.name = 'Arial Unicode MS'
    
    doc.save(output_docx)
    cv.close()
    print(f"Converted {input_pdf} to {output_docx}.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    select_pdf_file_and_convert()
