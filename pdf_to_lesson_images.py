import os
from pdf2image import convert_from_path

# ----------------------------
# Config
# ----------------------------
pdf_path = r"C:\Users\LENOVO\OneDrive\Documents\gAide\Gaide_learning_platform\subjects\Chemistry\Class_12_Chemistry_English_Medium-Volume_1-2024_Edition-www.tntextbooks.in.pdf"  # Your PDF
output_root = r"C:\Users\LENOVO\OneDrive\Documents\gAide\Gaide_learning_platform\subjects_Images\Chemistry\Class_12_Chemistry_English_Medium-Volume_1_Images"
poppler_path = r"C:\poppler\poppler-25.07.0\Library\bin"  # Your Poppler bin path

# Make sure output folder exists
os.makedirs(output_root, exist_ok=True)

# ----------------------------
# Convert PDF pages to images
# ----------------------------
pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)

for i, page in enumerate(pages, start=1):
    # Optional: organize by lesson if you have lesson info
    lesson_folder = os.path.join(output_root, f"Lesson_{i}")
    os.makedirs(lesson_folder, exist_ok=True)
    
    image_file = os.path.join(lesson_folder, f"page_{i}.png")
    page.save(image_file, "PNG")
    print(f"Saved {image_file}")

print("✅ PDF pages converted to images successfully!")
