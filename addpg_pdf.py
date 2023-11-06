import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ExifTags
import os
from io import BytesIO

class PDFEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor")
        self.root.configure(bg="black")  # Set the background color to black

        self.pdf_document = None
        self.current_page = 0
        self.temp_images = []  # List to hold temporary images to display

        self.create_gui()

    def create_gui(self):
        # Create navigation buttons
        self.prev_button = tk.Button(self.root, text="Previous Page", command=self.prev_page, bg="black", fg="white")
        self.next_button = tk.Button(self.root, text="Next Page", command=self.next_page, bg="black", fg="white")
        self.add_page_button = tk.Button(self.root, text="Add Page", command=self.add_page, bg="black", fg="white")
        self.add_to_last_page_button = tk.Button(self.root, text="Add to Last Page", command=self.add_to_last_page, bg="black", fg="white")
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
        self.add_page_button.pack()
        self.add_to_last_page_button.pack()
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
        if self.pdf_document is not None and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.show_page()

    def add_page(self):
        if self.pdf_document is not None:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
            if file_path:
                self.insert_page(file_path)
                self.show_page()  # Display the inserted page in the GUI

    def add_to_last_page(self):
        if self.pdf_document is not None:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
            if file_path:
                self.insert_page(file_path, page_index=len(self.pdf_document))  # Insert at the end
                self.show_page()  # Display the inserted page in the GUI

    def insert_page(self, image_path, page_index=None):
        if image_path:
            if page_index is None:
                page_index = self.current_page
            new_page = self.pdf_document.new_page(page_index, width=500, height=700)
            rect = fitz.Rect(0, 0, 500, 700)
            
            # Extract rotation information from the image (EXIF) and apply it to the new page
            img = Image.open(image_path)
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == "Orientation":
                        if value == 3:
                            new_page.set_rotation(180)
                        elif value == 6:
                            new_page.set_rotation(90)
                        elif value == 8:
                            new_page.set_rotation(270)
            
            image_pixmap = fitz.Pixmap(image_path)
            new_page.insert_image(rect, pixmap=image_pixmap)
            temp_image = Image.open(image_path)
            self.temp_images.insert(page_index, temp_image)

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
                messagebox.showinfo("PDF Saved", "PDF has been saved successfully.")
                self.root.quit()  # Exit the program

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditorApp(root)
    app.root.withdraw()  # Hide the GUI window initially
    app.load_pdf()
    root.mainloop()
