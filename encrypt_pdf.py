import PyPDF2

def encrypt_pdf(input_pdf, output_pdf, password):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Add all the pages from the input PDF to the writer
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        # Encrypt the PDF with a password
        pdf_writer.encrypt(password)

        # Write the encrypted PDF to the output file
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)

if __name__ == "__main__":
    input_pdf = 'input.pdf'
    output_pdf = 'output.pdf'
    password = 'apple'

    encrypt_pdf(input_pdf, output_pdf, password)
