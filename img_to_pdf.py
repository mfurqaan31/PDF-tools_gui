# gap issue fixed but make pdf needs to get fixed
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from fpdf import FPDF

class ImageDisplayApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")

        self.image_labels = []
        self.image_names = []

        # Create Open File Dialog Button
        self.open_button = tk.Button(self.master, text="Open Images", command=self.open_images)
        self.open_button.pack(pady=10)

        # Create Frames for left and right halves
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, padx=10)

        # Create Canvas to display images in the left frame
        self.canvas = tk.Canvas(self.left_frame, width=700, height=800)  # Adjust width and height as needed
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))  # Add right padding

        # Create Scrollbar for the Canvas
        self.canvas_scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.on_canvas_scroll)
        self.canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))  # Add left padding
        self.canvas.configure(yscrollcommand=self.canvas_scrollbar.set)

        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        # Create Listbox to display image names in the right frame
        self.listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE, width=30, height=20)
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Create Scrollbar for the Listbox
        self.listbox_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)

        # Create Buttons for image manipulation
        self.add_image_button = tk.Button(self.right_frame, text="Add Image", command=self.add_image)
        self.delete_image_button = tk.Button(self.right_frame, text="Delete Image", command=self.delete_image)
        self.move_up_button = tk.Button(self.right_frame, text="Move Up", command=self.move_up)
        self.move_down_button = tk.Button(self.right_frame, text="Move Down", command=self.move_down)
        self.make_pdf_button = tk.Button(self.right_frame, text="Make PDF", command=self.make_pdf)

        # Pack Buttons
        self.add_image_button.pack(pady=5)
        self.delete_image_button.pack(pady=5)
        self.move_up_button.pack(pady=5)
        self.move_down_button.pack(pady=5)
        self.make_pdf_button.pack(pady=5)

        # Track the current row and column positions
        self.current_row = 0
        self.current_col = 0

    def open_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.PNG *.JPEG")]
        )

        if file_paths:
            self.display_images(file_paths)

    def display_images(self, file_paths):
        # Load and display new images and names
        for i, file_path in enumerate(file_paths):
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
            tk_img = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=tk_img, text=file_path.split("/")[-1], compound=tk.TOP)
            label.grid(row=self.current_row, column=self.current_col, padx=5, pady=10)

            label.image = tk_img  # Keep a reference to avoid garbage collection
            self.image_labels.append(label)

            # Add image name to the listbox
            image_name = file_path.split("/")[-1]
            self.listbox.insert(tk.END, image_name)
            self.image_names.append(image_name)

            # Update current row and column positions
            self.current_col += 1
            if self.current_col == 3:
                self.current_row += 1
                self.current_col = 0

        self.image_frame.update_idletasks()  # Update the canvas with the new images
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Adjust the scroll region

    def on_canvas_scroll(self, *args):
        self.canvas.yview(*args)

    def add_image(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.PNG *.JPEG")]
        )

        if file_paths:
            # Reset current_row and current_col to append images at the end
            self.current_row = len(self.image_labels) // 3
            self.current_col = len(self.image_labels) % 3

            for file_path in file_paths:
                img = Image.open(file_path)
                img = img.resize((200, 200), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
                tk_img = ImageTk.PhotoImage(img)

                label = tk.Label(self.image_frame, image=tk_img, text=file_path.split("/")[-1], compound=tk.TOP)
                label.grid(row=self.current_row, column=self.current_col, padx=5, pady=10)

                label.image = tk_img  # Keep a reference to avoid garbage collection
                self.image_labels.append(label)

                # Add image name to the listbox
                image_name = file_path.split("/")[-1]
                self.listbox.insert(tk.END, image_name)
                self.image_names.append(image_name)

                # Update current row and column positions
                self.current_col += 1
                if self.current_col == 3:
                    self.current_row += 1
                    self.current_col = 0

            self.image_frame.update_idletasks()  # Update the canvas with the new images
            self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Adjust the scroll region

    def delete_image(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            deleted_image = self.image_names.pop(selected_index)
            self.listbox.delete(selected_index)

            # Find and destroy the label associated with the deleted image
            for label in self.image_labels:
                if label.cget("text") == deleted_image:
                    label.destroy()
                    self.image_labels.remove(label)
                    break

            # Update the canvas layout without creating gaps
            self.rearrange_images()

    def move_up(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            selected_index = selected_index[0]
            self.swap_items(selected_index, selected_index - 1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < self.listbox.size() - 1:
            selected_index = selected_index[0]
            self.swap_items(selected_index, selected_index + 1)

    def rearrange_images(self):
        # Clear the canvas
        for label in self.image_labels:
            label.grid_forget()

        # Redraw the images in proper order
        for i, label in enumerate(self.image_labels):
            row = i // 3
            col = i % 3
            self.image_frame.grid_rowconfigure(row, weight=1)
            self.image_frame.grid_columnconfigure(col, weight=1)
            label.grid(row=row, column=col, padx=5, pady=10)

        # Update the canvas and scroll region
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def swap_items(self, index1, index2):
        # Swap image names in the listbox
        self.image_names[index1], self.image_names[index2] = self.image_names[index2], self.image_names[index1]
        self.listbox.delete(0, tk.END)
        for image_name in self.image_names:
            self.listbox.insert(tk.END, image_name)

        # Swap labels in the canvas
        self.image_labels[index1], self.image_labels[index2] = self.image_labels[index2], self.image_labels[index1]
        self.rearrange_images()

    def make_pdf(self):
        if not self.image_names:
            print("No images selected. Nothing to create.")
            return

        pdf = FPDF()
        for image_name in self.image_names:
            pdf.add_page()
            image_path = [path for path in filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.PNG *.JPEG")]) if image_name in path][0]
            pdf.image(image_path, 10, 10, 190)

        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        pdf.output(pdf_file_path)
        print(f'PDF created and saved as "{pdf_file_path}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.mainloop()

