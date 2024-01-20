# main code
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os
import shutil
from zipfile import ZipFile

class PDFSplitterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Splitter")
        self.master.configure(bg="black")
        self.master.geometry("800x900")
        self.master.resizable(False, False)
        self.canvas = tk.Canvas(master, borderwidth=0, background="black", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.frame = tk.Frame(self.canvas, background="black")
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.file_path = None
        self.page_ranges = []
        self.pdf_name_label = tk.Label(self.frame, text="", bg="black", fg="white", font=("Helvetica", 16))
        self.pdf_name_label.pack(pady=20)
        tk.Label(self.frame, text="Page Ranges:", bg="black", fg="white", font=("Helvetica", 14)).pack(pady=10)
        self.add_range_button = tk.Button(self.frame, text="Add Range", command=self.add_page_range, bg="black", fg="white", font=("Helvetica", 14))
        self.add_range_button.pack(pady=10)
        self.merge_var = tk.BooleanVar()
        self.merge_checkbox = tk.Checkbutton(self.frame, text="Merge all ranges into a single PDF", variable=self.merge_var, bg="black", fg="white", font=("Helvetica", 14), selectcolor="black")
        self.merge_checkbox.pack(pady=10)
        tk.Button(self.frame, text="Split PDF", command=self.split_pdf, bg="black", fg="white", font=("Helvetica", 16)).pack(pady=20)
        self.master.iconify()
        self.master.withdraw()
        self.select_and_open_pdf()
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_window, width=event.width)

    def select_and_open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path = file_path
            self.pdf_name_label.config(text="Selected PDF: " + os.path.basename(self.file_path))
            self.master.deiconify()
        else:
            messagebox.showinfo("Error", "No PDF selected hence exiting")
            exit()

    def add_page_range(self):
        range_frame = tk.Frame(self.frame, bg="black")
        range_frame.pack(pady=5)
        tk.Label(range_frame, text=f"Range {len(self.page_ranges) + 1}:", bg="black", fg="white", font=("Helvetica", 14)).grid(row=0, column=0, pady=5)
        from_page_entry = tk.Entry(range_frame)
        to_page_entry = tk.Entry(range_frame)
        from_page_entry.grid(row=0, column=1, padx=5)
        to_page_entry.grid(row=0, column=2, padx=5)
        delete_button = tk.Button(range_frame, text="Delete", command=lambda frame=range_frame: self.delete_page_range(frame), bg="black", fg="white", font=("Helvetica", 14))
        delete_button.grid(row=0, column=3, padx=5)
        self.page_ranges.append((from_page_entry, to_page_entry, range_frame))

    def delete_page_range(self, frame):
        for i, (_, _, f) in enumerate(self.page_ranges):
            if f == frame:
                self.page_ranges.pop(i)
                frame.destroy()
                for j, (_, _, f) in enumerate(self.page_ranges):
                    f.pack(pady=5)
                    f.winfo_children()[0].config(text=f"Range {j + 1}:")
                break

    def split_pdf(self):
        if not self.file_path:
            messagebox.showinfo("Error", "No PDF selected hence exiting")
            exit()
        if not self.page_ranges:
            messagebox.showerror("Error", "Please add at least one page range.")
            return
        for i, (from_page_entry, to_page_entry, _) in enumerate(self.page_ranges):
            try:
                from_page = int(from_page_entry.get())
                to_page = int(to_page_entry.get())
                if from_page > to_page or from_page < 1 or to_page > len(PdfReader(self.file_path).pages):
                    raise ValueError("Invalid page range")
            except ValueError:
                messagebox.showerror("Error", f"Invalid page range for Range {i + 1}.")
                return
        output_folder = filedialog.asksaveasfilename(
            defaultextension=".zip" if not self.merge_var.get() else ".pdf",
            filetypes=[
                ("ZIP files" if not self.merge_var.get() else "PDF files",
                 "*.zip" if not self.merge_var.get() else "*.pdf")
            ],
            title="Save As"
        )
        if not output_folder:
            messagebox.showinfo("Error", "Enter location to store the output pdf")
            return
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_folder_path = os.path.join(os.path.dirname(output_folder), f"{file_name}_output")
        os.makedirs(output_folder_path, exist_ok=True)
        pdf_reader = PdfReader(self.file_path)
        for i, (from_page_entry, to_page_entry, _) in enumerate(self.page_ranges):
            from_page = int(from_page_entry.get())
            to_page = int(to_page_entry.get())
            pdf_writer = PdfWriter()
            for page_num in range(from_page - 1, to_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            output_file_path = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
            with open(output_file_path, "wb") as output_file:
                pdf_writer.write(output_file)
        if self.merge_var.get():
            merged_pdf_writer = PdfWriter()
            for i, (from_page_entry, to_page_entry, _) in enumerate(self.page_ranges):
                input_file_path = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
                input_pdf_reader = PdfReader(input_file_path)
                for page_num in range(len(input_pdf_reader.pages)):
                    merged_pdf_writer.add_page(input_pdf_reader.pages[page_num])
            merged_output_path = output_folder
            with open(merged_output_path, "wb") as merged_output_file:
                merged_pdf_writer.write(merged_output_file)
            shutil.rmtree(output_folder_path)
        else:
            zip_filename = output_folder
            with ZipFile(zip_filename, 'w') as zipf:
                for i, (from_page_entry, to_page_entry

, _) in enumerate(self.page_ranges):
                    pdf_filename = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
                    zipf.write(pdf_filename, os.path.basename(pdf_filename))
            shutil.rmtree(output_folder_path)
        messagebox.showinfo("Message", "PDF(s) successfully split and saved as " + output_folder.split("/")[-1] + " at " + os.path.dirname(output_folder))
        exit()

root = tk.Tk()
app = PDFSplitterApp(root)
root.mainloop()
