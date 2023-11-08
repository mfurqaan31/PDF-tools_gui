import PyPDF2
import tkinter as tk
from tkinter import Entry, Button, filedialog
import os

class PDFEncryptApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Encryption")

        # Set the GUI window size
        self.root.geometry("600x200")
        self.root.resizable(False,False)
        # Set the background color of the GUI window to black
        self.root.configure(bg="black")

        self.pdf_file = None

        self.create_gui()

    def create_gui(self):
        # Customize the labels and entry box appearance
        self.password_label = tk.Label(self.root, text="Enter Password:", fg="white", bg="black")
        self.password_label.pack()

        self.password_entry = Entry(self.root, bg="white")
        self.password_entry.pack(pady=5, ipadx=150)  # Adjust the entry box size

        self.encrypt_button = Button(self.root, text="Encrypt PDF", command=self.encrypt_pdf, state=tk.DISABLED)
        self.encrypt_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", fg="white", bg="black")
        self.result_label.pack()

    def select_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_file:
            self.password_entry.config(state=tk.NORMAL)
            self.encrypt_button.config(state=tk.NORMAL)
            self.root.deiconify()  # Display the GUI after selecting a PDF

    def encrypt_pdf(self):
        password = self.password_entry.get()

        if not self.pdf_file:
            print("Please select a PDF file first.")
            return

        # Create a PdfWriter to write the encrypted PDF
        pdf_writer = PyPDF2.PdfWriter()

        # Check if the PDF is already encrypted
        is_encrypted = False
        with open(self.pdf_file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            is_encrypted = pdf_reader.is_encrypted

        if is_encrypted:
            print("PDF is already encrypted.")
            self.root.destroy()

        else:
            # Open the input PDF file and add pages to the writer
            with open(self.pdf_file, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

            # Encrypt the PDF with the provided password
            pdf_writer.encrypt(password)

            default_output_file = f"encrypted_{os.path.basename(self.pdf_file)}"
            save_path = filedialog.asksaveasfilename(
                filetypes=[("PDF files", "*.pdf")],
                defaultextension=".pdf",
                initialfile=default_output_file,
            )

            if save_path:
                with open(save_path, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
                print(f"PDF encrypted and saved as {save_path}.")
                self.root.destroy()  # Close the GUI window and terminate the program
            else:
                print("PDF encryption canceled.")
                self.root.destroy()

    def run(self):
        self.root.withdraw()  # Hide the GUI window initially
        self.select_pdf()
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFEncryptApp()
    app.run()
