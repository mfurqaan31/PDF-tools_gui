# this needs to be fixed
from tkinter import Tk, filedialog
from PIL import Image, ExifTags
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def select_images():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_paths = filedialog.askopenfilenames(
        title="Select Images", filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All files", "*.*"))
    )

    return file_paths

def get_image_with_correct_orientation(image_path):
    img = Image.open(image_path)
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            try:
                exif = dict(img._getexif().items())
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
            except (AttributeError, KeyError):
                # If there is no orientation in the EXIF data, pass
                pass
    return img

def scale_to_fit_page(image, page_width, page_height):
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if img_width > page_width:
        img_width = page_width
        img_height = img_width / aspect_ratio

    if img_height > page_height:
        img_height = page_height
        img_width = img_height * aspect_ratio

    return image.resize((int(img_width), int(img_height)))

def create_centered_pdf(input_images, output_pdf):
    # Create a PDF canvas with letter page size
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for image_path in input_images:
        # Open the image using Pillow
        img = get_image_with_correct_orientation(image_path)

        # Convert the image to RGB mode
        img = img.convert("RGB")

        # Get the size of the image and the PDF page
        pdf_width, pdf_height = letter

        # Scale the image to fit within the PDF page
        img = scale_to_fit_page(img, pdf_width, pdf_height)

        # Calculate the position to center the image
        x = (pdf_width - img.width) / 2
        y = (pdf_height - img.height) / 2

        # Convert the image to a BytesIO object
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG")
        img_data = img_buffer.getvalue()
        img_buffer.close()

        # Add the image to the PDF canvas
        c.drawImage(ImageReader(BytesIO(img_data)), x, y, img.width, img.height)

        # Add a new page for the next image
        c.showPage()

    # Save the PDF file
    c.save()

if __name__ == "__main__":
    input_images = select_images()
    
    if not input_images:
        print("No images selected. Exiting.")
    else:
        output_pdf = "output.pdf"
        create_centered_pdf(input_images, output_pdf)
