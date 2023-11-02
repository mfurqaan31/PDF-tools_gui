import tkinter as tk
from tkinter import filedialog
from docx2pdf import convert
import os

def select_docx_file_and_convert():
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        # Extract the filename without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Set the output PDF path in the "Downloads" directory
        pdf_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name + ".pdf")
        
        convert(file_path, pdf_path)
        print(f"Converted {file_path} to {pdf_path}.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    select_docx_file_and_convert()
