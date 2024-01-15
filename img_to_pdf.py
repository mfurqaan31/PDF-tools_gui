# only encrypt image and gui theme needs to be fixed
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from fpdf import FPDF
from reportlab.pdfgen import canvas

image_location=[]

class ImageDisplayApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")

        self.image_labels = []
        self.image_names = []
        # self.image_location=[]

        # Store the selected label
        self.selected_label = None

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
        self.add_image_button.pack(pady=5,padx=15)
        self.delete_image_button.pack(pady=5,padx=15)
        self.move_up_button.pack(pady=5,padx=15)
        self.move_down_button.pack(pady=5,padx=15)
        self.make_pdf_button.pack(pady=5,padx=15)

        # Track the current row and column positions
        self.current_row = 0
        self.current_col = 0

        self.master.bind("<Left>", lambda event: self.move_up())
        self.master.bind("<Right>", lambda event: self.move_down())


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
                image_location.append(file_path)
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
            image_location.pop(selected_index)

            # Find and destroy the label associated with the deleted image
            for label in self.image_labels:
                if label.cget("text") == deleted_image:
                    label.destroy()
                    self.image_labels.remove(label)
                    break

            # Update the canvas layout without creating gaps
            self.rearrange_images()

    def move_up(self, positions=1):
        
        def reorder_pdf_files(old_index, new_index):
            image_location.insert(new_index, image_location.pop(old_index))

        if self.selected_label and self.selected_label in self.image_labels:
            selected_index = self.image_labels.index(self.selected_label)
            new_index = max(0, selected_index - positions)
            self.move_item(selected_index, new_index)
            reorder_pdf_files(selected_index, selected_index - 1)


    def move_down(self, positions=1):
        
        def reorder_pdf_files(old_index, new_index):
            image_location.insert(new_index, image_location.pop(old_index))
        
        if self.selected_label and self.selected_label in self.image_labels:
            selected_index = self.image_labels.index(self.selected_label)
            new_index = min(len(self.image_labels) - 1, selected_index + positions)
            self.move_item(selected_index, new_index)
            reorder_pdf_files(selected_index, selected_index + 1)
    

    def move_item(self, from_index, to_index):
        # Move image name in the listbox
        moved_name = self.image_names.pop(from_index)
        self.image_names.insert(to_index, moved_name)
        self.listbox.delete(0, tk.END)
        for image_name in self.image_names:
            self.listbox.insert(tk.END, image_name)

        # Move label in the canvas
        moved_label = self.image_labels.pop(from_index)
        self.image_labels.insert(to_index, moved_label)
        self.rearrange_images()

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
        
        def resize_and_paste(img, target_size):
            # Create a new image with a white background
            white_background = Image.new('RGB', target_size, 'white')

            # Calculate the position to center the image on the white background
            position = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)

            # Paste the original image onto the white background
            white_background.paste(img, position)

            return white_background

        def convert_images_to_pdf(image_paths, output_pdf_path, page_size=(800, 600)):
            # Create a new PDF document
            pdf_canvas = canvas.Canvas(output_pdf_path)

            for image_path in image_paths:
                # Open each image using Pillow
                img = Image.open(image_path)

                # Resize the image to fit into the specified page size while maintaining the aspect ratio
                img.thumbnail(page_size)

                # Calculate the position to center the image on the page
                position = ((page_size[0] - img.width) // 2, (page_size[1] - img.height) // 2)

                # Create a new image with a white background
                white_background = Image.new('RGB', page_size, 'white')

                # Paste the resized image onto the white background
                white_background.paste(img, position)

                # Set the size of the PDF page to the specified page size
                pdf_canvas.setPageSize(page_size)

                # Draw the image on the PDF
                pdf_canvas.drawInlineImage(white_background, 0, 0, width=page_size[0], height=page_size[1])

                # Add a new page for the next image
                pdf_canvas.showPage()

            # Save the PDF
            pdf_canvas.save()
        
        if not image_location:
            messagebox.showinfo("Error", "No images Selected")
            return
        
        pdf_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save PDF As")

        if not pdf_name:
            messagebox.showinfo("Error", "No Location Selected")
            return
        
        convert_images_to_pdf(image_location, pdf_name)
        messagebox.showinfo("Message","Images converted to PDF")
        exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    app.bind_listbox_select()  # Bind the listbox select callback
    root.mainloop()
