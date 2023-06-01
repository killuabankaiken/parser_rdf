import pytesseract
import PyPDF2
from pdf2image import convert_from_path
import csv
import cv2
import numpy as np
import os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

pdf_file = open('pdf_img.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)


with open('output.csv', mode='w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        width = int(page.mediabox[2])
        height = int(page.mediabox[3])

        pages = convert_from_path('pdf_img.pdf', dpi=200, first_page=page_num + 1,
                                  last_page=page_num + 1, poppler_path=r'D:\poppler-0.68.0\bin')
        img = pages[0]

        # Алгоритм преобр в серый отенок по Канни
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (3, 3), 0)
        #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Выдел контуры для опред области таблицы
        #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Перебрать все контуры и найти самый большой прямоугольный контур
        #max_area = 0
        #table_contour = None
        #for c in contours:
        #    area = cv2.contourArea(c)
        #    if area > max_area:
        #        perimeter = cv2.arcLength(c, True)
        #        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        #        if len(approx) == 4:
        #            max_area = area
        #            table_contour = approx

        # draw ограниц рамку
        #if table_contour is not None:
        #    cv2.drawContours(img, [table_contour], -1, (0, 255, 0), 2)
        #    cv2.imwrite("page_processed.png", img)


        temp_image = f"page{page_num}.png"
        img.save(temp_image)

        image_text = pytesseract.image_to_string(img)

        print(f"Page {page_num + 1}:")
        print(image_text)

        rows = image_text.strip().split('\n')
        for row in rows:
            cols = row.split()
            writer.writerow(cols)

        os.remove(temp_image)

pdf_file.close()
