import fitz  # PyMuPDF
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os
import platform

def convert_pdf_to_images(pdf_path, image_folder):
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        image_list = page.get_pixmap()

        # Convert the PyMuPDF image to a PIL image
        pil_image = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

        # Save the PIL image as a PNG file (you can change the format as needed)
        image_filename = os.path.join(image_folder, f"page_{page_number + 1}.png")
        pil_image.save(image_filename, "PNG")

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if file_path:
        # Get the current user's Downloads directory
        if platform.system() == 'Windows':
            downloads_dir = os.path.expanduser("~\\Downloads")
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            downloads_dir = os.path.expanduser("~/Downloads")
        else:
            # For other platforms, specify the downloads directory manually
            downloads_dir = "/path/to/downloads"

        # Extract the PDF file name without extension
        pdf_file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Create a subdirectory named after the PDF file
        image_folder = os.path.join(downloads_dir, f"pdf_img_{pdf_file_name}")

        if not os.path.exists(image_folder):
            os.mkdir(image_folder)

        convert_pdf_to_images(file_path, image_folder)
        print(f"PDF converted to images in {image_folder}")

select_pdf_file()