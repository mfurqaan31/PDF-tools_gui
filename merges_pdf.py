import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
import os
import platform

pdf_files = []
pdf_files_ordered = []

# Function to add a new PDF to the listbox
def add_pdf():
    new_pdf = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    if new_pdf:
        pdf_files.append(new_pdf)
        pdf_files_ordered.append(new_pdf)
        pdf_listbox.insert(tk.END, os.path.basename(new_pdf))

# Function to remove the selected PDF from the listbox
def remove_pdf():
    selected_index = pdf_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        pdf_listbox.delete(selected_index)
        removed_pdf = pdf_files_ordered.pop(selected_index)
        pdf_files.remove(removed_pdf)

# Function to move the selected item in the listbox up
def move_up():
    selected_index = pdf_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index > 0:
            item = pdf_listbox.get(selected_index)
            pdf_listbox.delete(selected_index)
            pdf_listbox.insert(selected_index - 1, item)
            pdf_listbox.select_set(selected_index - 1)
            reorder_pdf_files(selected_index, selected_index - 1)

# Function to move the selected item in the listbox down
def move_down():
    selected_index = pdf_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index < pdf_listbox.size() - 1:
            item = pdf_listbox.get(selected_index)
            pdf_listbox.delete(selected_index)
            pdf_listbox.insert(selected_index + 1, item)
            pdf_listbox.select_set(selected_index + 1)
            reorder_pdf_files(selected_index, selected_index + 1)

# Function to maintain the order of the PDF files based on listbox changes
def reorder_pdf_files(old_index, new_index):
    pdf_files_ordered.insert(new_index, pdf_files_ordered.pop(old_index))

# Function to merge the selected PDFs in the order specified
def merge_pdfs():
    if not pdf_files_ordered:
        print("No PDFs selected. Nothing to merge.")
        return

    # Determine the downloads directory based on the platform
    if platform.system() == 'Windows':
        downloads_dir = os.path.expanduser("~\\Downloads")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        downloads_dir = os.path.expanduser("~/Downloads")
    else:
        # For other platforms, specify the downloads directory manually
        downloads_dir = "/path/to/downloads"

    # Construct the output file path with the name of the first PDF file
    output_pdf = os.path.join(downloads_dir, f'combined_{os.path.splitext(os.path.basename(pdf_files[0]))[0]}.pdf')

    pdf_document = fitz.open()
    for pdf_file in pdf_files_ordered:
        pdf_document.insert_pdf(fitz.open(pdf_file))
    pdf_document.save(output_pdf)
    pdf_document.close()

    print(f'PDFs merged and saved as "{output_pdf}"')
    exit()

# Allow the user to select multiple PDFs from their PC
pdf_files = list(filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
))

if not pdf_files:
    print("No PDF files selected. Exiting.")
else:
    # Create a tkinter root window for the GUI
    root = tk.Tk()
    root.title("PDF Order")
    root.configure(bg='black')  # Set the background color to black
    root.resizable(False, False)  # Make the window non-resizable

    pdf_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg='white', fg='black', width=100, height=20)
    pdf_listbox.pack(padx=20, pady=10)
    pdf_listbox.config(highlightbackground='black')  # Set the listbox border color

    pdf_files_ordered = pdf_files.copy()  # To maintain the order of PDFs

    for pdf_file in pdf_files:
        pdf_listbox.insert(tk.END, os.path.basename(pdf_file))

    add_pdf_button = tk.Button(root, text="Add PDF", command=add_pdf, padx=20, pady=10)
    remove_pdf_button = tk.Button(root, text="Remove PDF", command=remove_pdf, padx=20, pady=10)
    move_up_button = tk.Button(root, text="Move Up", command=move_up, padx=20, pady=10)
    move_down_button = tk.Button(root, text="Move Down", command=move_down, padx=20, pady=10)
    merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs, padx=20, pady=10)

    add_pdf_button.pack(pady=10)
    remove_pdf_button.pack(pady=10)
    move_up_button.pack(pady=10)
    move_down_button.pack(pady=10)
    merge_button.pack(pady=10)

    root.mainloop()
