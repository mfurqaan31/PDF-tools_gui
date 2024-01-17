# main code
import fitz
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import PyPDF2
import zipfile
from io import BytesIO

def check_encrypted(pdf_path):

    is_encrypted = False
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        is_encrypted = pdf_reader.is_encrypted

    if is_encrypted:
        messagebox.showinfo("Error", "The selected PDF is encrypted hence cannot convert to images so exiting")
        exit()

def convert_pdf_to_zip(pdf_path, zip_filename):

    pdf_document = fitz.open(pdf_path)

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            image_list = page.get_pixmap()

            pil_image = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

            image_filename = f"page_{page_number + 1}.png"
            with BytesIO() as image_bytes:
                pil_image.save(image_bytes, format="PNG")
                image_data = image_bytes.getvalue()
                zip_file.writestr(image_filename, image_data)

    messagebox.showinfo("Message", "The PDF converted to images and saved as " + zip_filename.split("/")[-1] + " at " + os.path.dirname(zip_filename))

def select_pdf_and_save_zip():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    check_encrypted(file_path)

    if file_path:
        zip_filename = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])

        if zip_filename:
            convert_pdf_to_zip(file_path, zip_filename)
        else:
            messagebox.showinfo("Message", "No Location Selected")
            exit()
    else:
        messagebox.showinfo("Error", "No PDF selected Exiting")
        exit()

select_pdf_and_save_zip()
