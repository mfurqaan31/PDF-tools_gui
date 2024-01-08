import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
import os
import platform

pdf_files = []
pdf_files_ordered = []

# Function to add a new PDF to the listbox
def add_pdf():
    new_pdf = list(filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
))
    if new_pdf:
        for i in new_pdf:
            pdf_files.append(i)
            pdf_files_ordered.append(i)
            pdf_listbox.insert(tk.END, os.path.basename(i))

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

# Function to check if a PDF is encrypted
def is_encrypted(pdf_path):
    pdf_document = fitz.open(pdf_path)
    encrypted = pdf_document.is_encrypted
    pdf_document.close()
    return encrypted

# Function to merge the selected PDFs in the order specified
def merge_pdfs():
    if not pdf_files_ordered:
        print("No PDFs selected. Nothing to merge.")
        return

    encrypted_files = []
    for pdf_file in pdf_files_ordered:
        if is_encrypted(pdf_file):
            encrypted_files.append(os.path.basename(pdf_file))
    
    if encrypted_files:
        message = f"{', '.join(encrypted_files)} {'is' if len(encrypted_files) == 1 else 'are'} encrypted."
        print(message)
        # Display the message in the GUI window
        messagebox.showinfo("Encrypted PDFs", message)
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

    # Create a frame to contain the listbox and scrollbar
    frame = tk.Frame(root)
    frame.pack()

    # Create a vertical scrollbar
    scrollbar = Scrollbar(frame, orient="vertical")

    root.bind("<Up>", lambda event: move_up())
    root.bind("<Down>", lambda event: move_down())

    # Create a listbox with the scrollbar attached
    pdf_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg='white', fg='black', width=100, height=20, yscrollcommand=scrollbar.set)
    pdf_listbox.grid(row=0, column=0)

    # Attach the scrollbar to the listbox
    scrollbar.config(command=pdf_listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

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
