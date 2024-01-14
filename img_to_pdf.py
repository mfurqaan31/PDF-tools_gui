# scroll works and append also works
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.mainloop()
