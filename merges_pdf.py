# main code
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
import os
import platform

pdf_files = []
pdf_files_ordered = []

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

def remove_pdf():

    selected_index = pdf_listbox.curselection()

    if selected_index:
        selected_index = selected_index[0]
        pdf_listbox.delete(selected_index)
        removed_pdf = pdf_files_ordered.pop(selected_index)
        pdf_files.remove(removed_pdf)

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

def reorder_pdf_files(old_index, new_index):

    pdf_files_ordered.insert(new_index, pdf_files_ordered.pop(old_index))

def is_encrypted(pdf_path):

    pdf_document = fitz.open(pdf_path)
    encrypted = pdf_document.is_encrypted
    pdf_document.close()
    return encrypted

def merge_pdfs():

    if not pdf_files_ordered:
        messagebox.showinfo("Error", "No PDFs selected. Nothing to merge.")
        return

    encrypted_files = []

    for pdf_file in pdf_files_ordered:
        if is_encrypted(pdf_file):
            encrypted_files.append(os.path.basename(pdf_file))

    if encrypted_files:
        message = f"{', '.join(encrypted_files)} {'is' if len(encrypted_files) == 1 else 'are'} encrypted."
        messagebox.showinfo("Encrypted PDFs", message + " Hence cannot merge PDFs so remove them")
        return

    pdf_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save PDF As")

    if not pdf_name:
        messagebox.showinfo("Message", "No Location Selected")
        return

    pdf_document = fitz.open()
    for pdf_file in pdf_files_ordered:
        pdf_document.insert_pdf(fitz.open(pdf_file))
    pdf_document.save(pdf_name)
    pdf_document.close()

    messagebox.showinfo("Message", "PDFs merged and saved as " + pdf_name.split("/")[-1] + " at " + os.path.dirname(pdf_name))
    exit()

pdf_files = list(filedialog.askopenfilenames(
    title="Select PDF Files",
    filetypes=[("PDF files", "*.pdf")]
))

if not pdf_files:

    messagebox.showinfo("Error", "No PDFs selected. Exiting")
    exit()
else:

    root = tk.Tk()
    root.title("PDF Order")
    root.configure(bg='black')
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack()

    scrollbar = Scrollbar(frame, orient="vertical")

    root.bind("<Up>", lambda event: move_up())
    root.bind("<Down>", lambda event: move_down())

    pdf_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg='white', fg='black', width=100, height=20, yscrollcommand=scrollbar.set, selectbackground="blue")
    pdf_listbox.grid(row=0, column=0)

    scrollbar.config(command=pdf_listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    pdf_listbox.config(highlightbackground='black')

    pdf_files_ordered = pdf_files.copy()

    for pdf_file in pdf_files:
        pdf_listbox.insert(tk.END, os.path.basename(pdf_file))

    button_width = 15

    add_pdf_button = tk.Button(root, text="Add PDF", command=add_pdf, padx=20, pady=10, width=button_width, bg="white", fg="black")
    remove_pdf_button = tk.Button(root, text="Remove PDF", command=remove_pdf, padx=20, pady=10, width=button_width, bg="white", fg="black")
    move_up_button = tk.Button(root, text="Move Up", command=move_up, padx=20, pady=10, width=button_width, bg="white", fg="black")
    move_down_button = tk.Button(root, text="Move Down", command=move_down, padx=20, pady=10, width=button_width, bg="white", fg="black")
    merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs, padx=20, pady=10, width=button_width, bg="white", fg="black")

    add_pdf_button.pack(pady=10)
    remove_pdf_button.pack(pady=10)
    move_up_button.pack(pady=10)
    move_down_button.pack(pady=10)
    merge_button.pack(pady=10)

    root.mainloop()
