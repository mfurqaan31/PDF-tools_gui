"""
import PyPDF2
import tkinter as tk
from tkinter import filedialog

# Create a tkinter root window (it won't be displayed)
root = tk.Tk()
root.withdraw()

# Prompt the user to select PDF files from a folder
pdf_files = filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
)

if not pdf_files:
    print("No PDF files selected. Exiting.")
    exit()

# Create a PDF merger object
pdf_merger = PyPDF2.PdfMerger()

# Iterate through the list of selected PDF files and append them to the merger
for pdf_file in pdf_files:
    pdf_merger.append(pdf_file)

# Output file name for the combined PDF
output_pdf = 'combined.pdf'

# Write the combined PDF to the output file
with open(output_pdf, 'wb') as output:
    pdf_merger.write(output)

# Close the PDF merger
pdf_merger.close()

print(f'Combined PDF saved as "{output_pdf}"')

"""




"""
# in downloads
import PyPDF2
from tkinter import filedialog
import tkinter as tk
import os
import platform

# Create a tkinter root window (it won't be displayed)
root = tk.Tk()
root.withdraw()

# Prompt the user to select PDF files from a folder
pdf_files = filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
)

if not pdf_files:
    print("No PDF files selected. Exiting.")
    exit()

# Get the name of the first selected PDF file
first_pdf_name = os.path.basename(pdf_files[0])

# Determine the downloads directory based on the platform
if platform.system() == 'Windows':
    downloads_dir = os.path.expanduser("~\\Downloads")
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    downloads_dir = os.path.expanduser("~/Downloads")
else:
    # For other platforms, specify the downloads directory manually
    downloads_dir = "/path/to/downloads"

# Construct the output file path with the name of the first PDF file
output_pdf = os.path.join(downloads_dir, f'{os.path.splitext(first_pdf_name)[0]}_merged.pdf')

# Create a PDF merger object
pdf_merger = PyPDF2.PdfMerger()

# Iterate through the list of selected PDF files and append them to the merger
for pdf_file in pdf_files:
    try:
        pdf_merger.append(pdf_file)
    except PyPDF2.utils.PdfReadError as e:
        print(f"Error appending {pdf_file}: {e}")

# Write the combined PDF to the output file
with open(output_pdf, 'wb') as output:
    pdf_merger.write(output)

# Close the PDF merger
pdf_merger.close()

print(f'Combined PDF saved as "{output_pdf}"')
"""

"""

import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
import os

# Create a tkinter root window (it won't be displayed)
root = tk.Tk()
root.withdraw()

# Prompt the user to select PDF files from a folder
pdf_files = filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
)

if not pdf_files:
    print("No PDF files selected. Exiting.")
    exit()

# Get the name of the first selected PDF file
first_pdf_name = pdf_files[0]

# Construct the output file path with the name of the first PDF file
output_pdf = f'combined_{os.path.splitext(os.path.basename(first_pdf_name))[0]}.pdf'

pdf_document = fitz.open()

# Iterate through the list of selected PDF files and insert them into the document
for pdf_file in pdf_files:
    pdf_document.insert_pdf(fitz.open(pdf_file))

pdf_document.save(output_pdf)
pdf_document.close()

print(f'Combined PDF saved as "{output_pdf}"')
"""

import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
import os
import platform

# Create a tkinter root window (it won't be displayed)
root = tk.Tk()
root.withdraw()

# Prompt the user to select PDF files from a folder
pdf_files = filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
)

if not pdf_files:
    print("No PDF files selected. Exiting.")
    exit()

# Get the name of the first selected PDF file
first_pdf_name = pdf_files[0]

# Determine the downloads directory based on the platform
if platform.system() == 'Windows':
    downloads_dir = os.path.expanduser("~\\Downloads")
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    downloads_dir = os.path.expanduser("~/Downloads")
else:
    # For other platforms, specify the downloads directory manually
    downloads_dir = "/path/to/downloads"

# Construct the output file path with the name of the first PDF file
output_pdf = os.path.join(downloads_dir, f'combined_{os.path.splitext(os.path.basename(first_pdf_name))[0]}.pdf')

pdf_document = fitz.open()

# Iterate through the list of selected PDF files and insert them into the document
for pdf_file in pdf_files:
    pdf_document.insert_pdf(fitz.open(pdf_file))

pdf_document.save(output_pdf)
pdf_document.close()

print(f'Combined PDF saved as "{output_pdf}"')
