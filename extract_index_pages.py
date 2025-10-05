# extract_index_pages.py
import pytesseract
from pdf2image import convert_from_path
import cv2
import re
import os

# 🧠 If tesseract is not in PATH, set it manually (Windows default below)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pdf_path="C:\\Users\\LENOVO\\OneDrive\\Documents\\gAide\\Gaide_learning_platform\\subjects\\Chemistry"
def extract_index_from_pdf(pdf_path):
    print("📖 Extracting index from:", pdf_path)
    pages = convert_from_path(pdf_path, 300, poppler_path=r"C:\\poppler\\poppler-25.07.0\\Library\bin")
    all_text = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        all_text += "\n" + text

    # Example pattern: "1 Metallurgy 01 June" → ("Metallurgy", 1)
    pattern = re.compile(r'\d+\s+([A-Za-z\s\-&]+)\s+(\d+)')
    lessons = []
    for match in pattern.findall(all_text):
        title = match[0].strip()
        page_num = int(match[1])
        lessons.append((title, page_num))

    lessons.sort(key=lambda x: x[1])
    print(f"✅ Found {len(lessons)} lessons:")
    for title, page in lessons:
        print(f" - {title} → Page {page}")

    # Save as a reference file
    with open("lesson_index.txt", "w", encoding="utf-8") as f:
        for title, page in lessons:
            f.write(f"{title}|{page}\n")

    return lessons


if __name__ == "__main__":
    pdf_path = input("Enter index PDF file path: ").strip('"')
    extract_index_from_pdf(pdf_path)
