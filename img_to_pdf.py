# main code
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from fpdf import FPDF
from reportlab.pdfgen import canvas
import os

image_location = []

class ImageDisplayApp:

    def __init__(self, master):

        self.master = master
        self.master.title("Image Viewer")
        self.master.configure(bg="black")
        self.image_labels = []
        self.image_names = []
        self.selected_label = None
        self.left_frame = tk.Frame(self.master, bg="black")
        self.left_frame.pack(side=tk.LEFT, padx=(0, 200))
        self.right_frame = tk.Frame(self.master, bg="black")
        self.right_frame.pack(side=tk.RIGHT, padx=10)
        self.canvas = tk.Canvas(self.left_frame, width=650, height=800, bg="black")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.canvas_scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.on_canvas_scroll)
        self.canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        self.canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.image_frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE, width=30, height=20, bg="white", fg="black", selectbackground="blue")
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.listbox_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        button_width = 15
        self.add_image_button = tk.Button(self.right_frame, text="Add Image", command=self.add_image, width=button_width, bg="white", fg="black")
        self.delete_image_button = tk.Button(self.right_frame, text="Delete Image", command=self.delete_image, width=button_width, bg="white", fg="black")
        self.move_up_button = tk.Button(self.right_frame, text="Move Up", command=self.move_up, width=button_width, bg="white", fg="black")
        self.move_down_button = tk.Button(self.right_frame, text="Move Down", command=self.move_down, width=button_width, bg="white", fg="black")
        self.make_pdf_button = tk.Button(self.right_frame, text="Make PDF", command=self.make_pdf, width=button_width, bg="white", fg="black")
        self.add_image_button.pack(pady=(70, 20), padx=(50, 10))
        self.delete_image_button.pack(pady=(0, 20), padx=(50, 10))
        self.move_up_button.pack(pady=(0, 20), padx=(50, 10))
        self.move_down_button.pack(pady=(0, 20), padx=(50, 10))
        self.make_pdf_button.pack(pady=(0, 20), padx=(50, 10))
        self.current_row = 0
        self.current_col = 0
        self.master.bind("<Up>", lambda event: self.move_up())
        self.master.bind("<Down>", lambda event: self.move_down())
        self.bind_listbox_select()

    def display_images(self, file_paths):

        for i, file_path in enumerate(file_paths):
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(self.image_frame, image=tk_img, text=file_path.split("/")[-1], compound=tk.TOP, bg="black", fg="white")
            label.grid(row=self.current_row, column=self.current_col, padx=5, pady=10)
            label.image = tk_img
            self.image_labels.append(label)
            image_name = file_path.split("/")[-1]
            self.listbox.insert(tk.END, image_name)
            self.image_names.append(image_name)
            self.current_col += 1
            if self.current_col == 3:
                self.current_row += 1
                self.current_col = 0
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_canvas_scroll(self, *args):

        self.canvas.yview(*args)

    def add_image(self):

        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.PNG *.JPEG")]
        )
        if file_paths:
            self.current_row = len(self.image_labels) // 3
            self.current_col = len(self.image_labels) % 3
            for file_path in file_paths:
                image_location.append(file_path)
                img = Image.open(file_path)
                img = img.resize((200, 200), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
                tk_img = ImageTk.PhotoImage(img)
                label = tk.Label(self.image_frame, image=tk_img, text=file_path.split("/")[-1], compound=tk.TOP, bg="black", fg="white")
                label.grid(row=self.current_row, column=self.current_col, padx=5, pady=10)
                label.image = tk_img
                self.image_labels.append(label)
                image_name = file_path.split("/")[-1]
                self.listbox.insert(tk.END, image_name)
                self.image_names.append(image_name)
                self.current_col += 1
                if self.current_col == 3:
                    self.current_row += 1
                    self.current_col = 0
            self.image_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def delete_image(self):

        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            deleted_image = self.image_names.pop(selected_index)
            self.listbox.delete(selected_index)
            image_location.pop(selected_index)
            for label in self.image_labels:
                if label.cget("text") == deleted_image:
                    label.destroy()
                    self.image_labels.remove(label)
                    break
            self.rearrange_images()

    def move_up(self, positions=1):

        def reorder_pdf_files(old_index, new_index):
            image_location.insert(new_index, image_location.pop(old_index))
        if self.selected_label and self.selected_label in self.image_labels:
            selected_index = self.image_labels.index(self.selected_label)
            new_index = max(0, selected_index - positions)
            if selected_index != new_index:
                self.move_item(selected_index, new_index)
                reorder_pdf_files(selected_index, new_index)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(new_index)
                self.listbox.yview(new_index)

    def move_down(self, positions=1):

        def reorder_pdf_files(old_index, new_index):

            image_location.insert(new_index, image_location.pop(old_index))
        if self.selected_label and self.selected_label in self.image_labels:
            selected_index = self.image_labels.index(self.selected_label)
            new_index = min(len(self.image_labels) - 1, selected_index + positions)
            if selected_index != new_index:
                self.move_item(selected_index, new_index)
                reorder_pdf_files(selected_index, new_index)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(new_index)
                self.listbox.yview(new_index)

    def move_item(self, from_index, to_index):

        moved_name = self.image_names.pop(from_index)
        self.image_names.insert(to_index, moved_name)
        self.listbox.delete(0, tk.END)
        for image_name in self.image_names:
            self.listbox.insert(tk.END, image_name)
        moved_label = self.image_labels.pop(from_index)
        self.image_labels.insert(to_index, moved_label)
        self.rearrange_images()

    def rearrange_images(self):

        for label in self.image_labels:
            label.grid_forget()
        for i, label in enumerate(self.image_labels):
            row = i // 3
            col = i % 3
            self.image_frame.grid_rowconfigure(row, weight=1)
            self.image_frame.grid_columnconfigure(col, weight=1)
            label.grid(row=row, column=col, padx=5, pady=10)
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def bind_listbox_select(self):

        self.listbox.bind('<<ListboxSelect>>', self.listbox_select_callback)

    def listbox_select_callback(self, event):

        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_image_name = self.listbox.get(selected_index)
            for label in self.image_labels:
                if label.cget("text") == selected_image_name:
                    self.selected_label = label
                    break

    def make_pdf(self):

        def convert_images_to_pdf(image_paths, output_pdf_path, page_size=(800, 600)):
            pdf_canvas = canvas.Canvas(output_pdf_path)
            for image_path in image_paths:
                img = Image.open(image_path)
                img.thumbnail(page_size)
                position = ((page_size[0] - img.width) // 2, (page_size[1] - img.height) // 2)
                white_background = Image.new('RGB', page_size, 'white')
                white_background.paste(img, position)
                pdf_canvas.setPageSize(page_size)
                pdf_canvas.drawInlineImage(white_background, 0, 0, width=page_size[0], height=page_size[1])
                pdf_canvas.showPage()
            pdf_canvas.save()

        if not image_location:
            messagebox.showinfo("Error", "No images Selected")
            return

        pdf_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save PDF As")
        if not pdf_name:
            messagebox.showinfo("Error", "No Location Selected")
            return

        convert_images_to_pdf(image_location, pdf_name)
        messagebox.showinfo("Message", "Images converted to PDF and saved as "+pdf_name.split("/")[-1] + " at " + os.path.dirname(pdf_name))
        exit()

if __name__ == "__main__":

    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.PNG *.JPEG")]
    )

    if not file_paths:
        messagebox.showinfo("Error", "No images selected. Exiting.")
        exit()

    image_location = list(file_paths)
    root = tk.Tk()
    root.resizable(False, False)
    app = ImageDisplayApp(root)
    app.bind_listbox_select()
    app.display_images(file_paths)
    root.mainloop()
