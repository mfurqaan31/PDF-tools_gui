# this needs to be fixed
import fitz
import os
import platform
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk

images = []
images_ordered = []

# Function to add a new image to the listbox
def add_image():
    new_image = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if new_image:
        images.append(new_image)
        images_ordered.append(new_image)
        image_name = os.path.basename(new_image)
        image_listbox.insert(tk.END, image_name)

# Function to remove the selected image from the listbox
def remove_image():
    selected_index = image_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        image_listbox.delete(selected_index)
        removed_image = images_ordered.pop(selected_index)
        images.remove(removed_image)

# Function to move the selected item in the listbox up
def move_up():
    selected_index = image_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index > 0:
            item = image_listbox.get(selected_index)
            image_listbox.delete(selected_index)
            image_listbox.insert(selected_index - 1, item)
            image_listbox.select_set(selected_index - 1)
            reorder_images(selected_index, selected_index - 1)

# Function to move the selected item in the listbox down
def move_down():
    selected_index = image_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index < image_listbox.size() - 1:
            item = image_listbox.get(selected_index)
            image_listbox.delete(selected_index)
            image_listbox.insert(selected_index + 1, item)
            image_listbox.select_set(selected_index + 1)
            reorder_images(selected_index, selected_index + 1)

# Function to maintain the order of the images based on listbox changes
def reorder_images(old_index, new_index):
    images_ordered.insert(new_index, images_ordered.pop(old_index))

# Function to merge the selected images in the order specified into a PDF
def merge_images_to_pdf():
    if not images_ordered:
        print("No images selected. Nothing to merge.")
        return

    # Determine the downloads directory based on the platform
    if platform.system() == 'Windows':
        downloads_dir = os.path.expanduser("~\\Downloads")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        downloads_dir = os.path.expanduser("~/Downloads")
    else:
        # For other platforms, specify the downloads directory manually
        downloads_dir = "/path/to/downloads"

    # Construct the output file path with the name of the first image file
    output_pdf = os.path.join(downloads_dir, f'combined_images.pdf')

    pdf_document = fitz.open()
    for image_file in images_ordered:
        img = Image.open(image_file)
        img = img.convert("RGB")
        img.save("temp.pdf", save_all=True, append_images=[img])
        pdf_document.insert_pdf(fitz.open("temp.pdf"))
        os.remove("temp.pdf")

    pdf_document.save(output_pdf)
    pdf_document.close()

    print(f'Images merged and saved as "{output_pdf}"')
    exit()

# Allow the user to select multiple images from their PC
images = list(filedialog.askopenfilenames(
    title="Select Image Files",
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
))

if not images:
    print("No image files selected. Exiting.")
else:
    # Create a tkinter root window for the GUI
    root = tk.Tk()
    root.title("Image Order")
    root.configure(bg='black')  # Set the background color to black
    root.resizable(False, False)  # Make the window non-resizable

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    image_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg='white', fg='black', width=50, height=10, yscrollcommand=scrollbar.set)
    image_listbox.pack(side=tk.LEFT)
    image_listbox.config(highlightbackground='black')  # Set the listbox border color

    scrollbar.config(command=image_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    images_ordered = images.copy()  # To maintain the order of images

    for image_file in images:
        image_name = os.path.basename(image_file)
        image_listbox.insert(tk.END, image_name)

    add_image_button = tk.Button(root, text="Add Image", command=add_image, padx=20, pady=10)
    remove_image_button = tk.Button(root, text="Remove Image", command=remove_image, padx=20, pady=10)
    move_up_image_button = tk.Button(root, text="Move Up", command=move_up, padx=20, pady=10)
    move_down_image_button = tk.Button(root, text="Move Down", command=move_down, padx=20, pady=10)
    merge_images_button = tk.Button(root, text="Merge Images to PDF", command=merge_images_to_pdf, padx=20, pady=10)

    add_image_button.pack(pady=10)
    remove_image_button.pack(pady=10)
    move_up_image_button.pack(pady=10)
    move_down_image_button.pack(pady=10)
    merge_images_button.pack(pady=10)

    root.mainloop()
