# added scrollbar
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

        # Create a canvas to contain the GUI widgets
        self.canvas = tk.Canvas(master, borderwidth=0, background="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to contain the scrollable content
        self.frame = tk.Frame(self.canvas, background="#ffffff")

        # Create a scrollbar and attach it to the canvas
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Assign the frame to the canvas
        self.frame_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Variables
        self.file_path = None
        self.page_ranges = []

        # Display PDF Name
        self.pdf_name_label = tk.Label(self.frame, text="")
        self.pdf_name_label.grid(row=0, column=0, padx=10, pady=10)

        # Page Ranges
        tk.Label(self.frame, text="Page Ranges:").grid(row=1, column=0, pady=10)
        self.add_range_button = tk.Button(self.frame, text="Add Range", command=self.add_page_range)
        self.add_range_button.grid(row=1, column=1, pady=10)

        # Merge Option
        self.merge_var = tk.BooleanVar()
        tk.Checkbutton(self.frame, text="Merge all ranges into a single PDF", variable=self.merge_var).grid(row=2, column=0, columnspan=3, pady=10)

        # Split Button
        tk.Button(self.frame, text="Split PDF", command=self.split_pdf).grid(row=3, column=0, columnspan=3, pady=10)

        # Bind the canvas to the scrollable area
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Hide the main window initially
        self.master.iconify()

        # Call the function to select and open the PDF
        self.select_and_open_pdf()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_window, width=event.width)

    def select_and_open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path = file_path
            self.pdf_name_label.config(text=os.path.basename(self.file_path))
            self.show_main_window()

    def show_main_window(self):
        self.master.deiconify()

    def add_page_range(self):
        range_frame = tk.Frame(self.frame)
        range_frame.grid(row=len(self.page_ranges) + 4, column=0, columnspan=3, pady=5)

        tk.Label(range_frame, text=f"Range {len(self.page_ranges) + 1}:").grid(row=0, column=0, pady=5)
        from_page_entry = tk.Entry(range_frame)
        to_page_entry = tk.Entry(range_frame)
        from_page_entry.grid(row=0, column=1, padx=5)
        to_page_entry.grid(row=0, column=2, padx=5)

        self.page_ranges.append((from_page_entry, to_page_entry))

    def split_pdf(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        output_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(output_folder, exist_ok=True)

        # Extract filename without extension
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]

        # Modify output folder name
        output_folder_path = os.path.join(output_folder, f"split_pages_{file_name}")
        os.makedirs(output_folder_path, exist_ok=True)

        pdf_reader = PdfReader(self.file_path)

        for i, (from_page_entry, to_page_entry) in enumerate(self.page_ranges):
            try:
                from_page = int(from_page_entry.get())
                to_page = int(to_page_entry.get())
                if from_page > to_page or from_page < 1 or to_page > len(pdf_reader.pages):
                    raise ValueError("Invalid page range")
            except ValueError:
                messagebox.showerror("Error", f"Invalid page range for Range {i + 1}.")
                return

            pdf_writer = PdfWriter()
            for page_num in range(from_page - 1, to_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file_path = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
            with open(output_file_path, "wb") as output_file:
                pdf_writer.write(output_file)

        if self.merge_var.get():
            merged_pdf_writer = PdfWriter()
            for i in range(len(self.page_ranges)):
                input_file_path = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
                input_pdf_reader = PdfReader(input_file_path)

                for page_num in range(len(input_pdf_reader.pages)):
                    merged_pdf_writer.add_page(input_pdf_reader.pages[page_num])

            merged_output_path = os.path.join(output_folder, f"Merged_Split_{file_name}.pdf")
            with open(merged_output_path, "wb") as merged_output_file:
                merged_pdf_writer.write(merged_output_file)

            shutil.rmtree(output_folder_path)  # Remove the individual PDFs if merged
        else:
            zip_filename = os.path.join(output_folder, f"Split_PDFs_{file_name}.zip")
            with ZipFile(zip_filename, 'w') as zipf:
                for i in range(len(self.page_ranges)):
                    pdf_filename = os.path.join(output_folder_path, f"Range_{i + 1}.pdf")
                    zipf.write(pdf_filename, os.path.basename(pdf_filename))

            shutil.rmtree(output_folder_path)  # Remove the individual PDFs if zipped

        messagebox.showinfo("Success", "PDF(s) successfully split.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
