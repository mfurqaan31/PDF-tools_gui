import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class PDFEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor")
        self.root.configure(bg="black")  # Set the background color to black

        self.pdf_document = None
        self.current_page = 0

        self.create_gui()

    def create_gui(self):
        # Create navigation buttons
        self.prev_button = tk.Button(self.root, text="Previous Page", command=self.prev_page, bg="black", fg="white")
        self.next_button = tk.Button(self.root, text="Next Page", command=self.next_page, bg="black", fg="white")
        self.delete_button = tk.Button(self.root, text="Delete Page", command=self.delete_page, bg="black", fg="white")
        self.make_pdf_button = tk.Button(self.root, text="Make PDF", command=self.save_pdf, bg="black", fg="white")

        # Create a canvas to display the PDF page
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="black")  # Set canvas background color to black
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, bg="black")  # Set scrollbar background color to black
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Pack buttons
        self.prev_button.pack()
        self.next_button.pack()
        self.delete_button.pack()
        self.make_pdf_button.pack()

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0
            self.show_page()
            self.root.deiconify()  # Show the GUI window after selecting a PDF

    def show_page(self):
        if self.pdf_document is not None:
            page = self.pdf_document.load_page(self.current_page)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            self.tk_image = ImageTk.PhotoImage(img)
            canvas_width = img.width
            canvas_height = img.height
            self.canvas.config(width=canvas_width, height=canvas_height)  # Adjust canvas size
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.show_page()

    def delete_page(self):
        if self.pdf_document is not None:
            if len(self.pdf_document) > 1:
                self.pdf_document.delete_page(self.current_page)
                if self.current_page >= len(self.pdf_document):
                    self.current_page = len(self.pdf_document) - 1
                self.show_page()
            else:
                messagebox.showwarning("Cannot Delete Page", "Cannot delete the last page.")

    def save_pdf(self):
        if self.pdf_document is not None:
            default_file_name = "output.pdf"
            save_path = filedialog.asksaveasfilename(
                filetypes=[("PDF files", "*.pdf")],
                defaultextension=".pdf",
                initialfile=default_file_name,
                initialdir=os.path.expanduser("~\\Downloads")
            )

            if save_path:
                self.pdf_document.save(save_path)
                self.pdf_document.close()
                self.pdf_document = fitz.open(save_path)
                self.current_page = 0
                self.show_page()
                messagebox.showinfo("PDF Saved", "PDF has been saved successfully.")
                self.root.quit()  # Exit the program

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditorApp(root)
    root.withdraw()  # Hide the GUI window initially
    app.load_pdf()
    root.mainloop()
