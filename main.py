import pytesseract
import PyPDF2
from pdf2image import convert_from_path
import os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

pdf_file = open('pdf_img.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

print(f"Number of pages: {len(pdf_reader.pages)}")
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    width = int(page.mediabox[2])
    height = int(page.mediabox[3])

    text = page.extract_text()

    pages = convert_from_path('pdf_img.pdf', dpi=200, first_page=page_num + 1, last_page=page_num + 1,poppler_path=r'D:\poppler-0.68.0\bin')
    img = pages[0]
    temp_image = f"page{page_num}.png"
    img.save(temp_image)

    image_text = pytesseract.image_to_string(img)

    print(f"Page {page_num + 1}:")
    print(image_text)

    os.remove(temp_image)

pdf_file.close()