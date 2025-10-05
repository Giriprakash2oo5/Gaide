# split_pdf_by_lessons.py
from PyPDF2 import PdfReader, PdfWriter
import os

def load_lessons(index_file="lesson_index.txt"):
    lessons = []
    with open(index_file, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                title, page = line.strip().split("|")
                lessons.append((title, int(page)))
    return lessons


def split_pdf_by_lessons(pdf_path, lessons):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    output_dir = "lessons_split"
    os.makedirs(output_dir, exist_ok=True)

    for i, (title, start_page) in enumerate(lessons):
        end_page = lessons[i + 1][1] - 1 if i + 1 < len(lessons) else total_pages
        writer = PdfWriter()
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

        safe_title = title.replace(" ", "_").replace("/", "_")
        output_path = os.path.join(output_dir, f"{safe_title}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"✅ Saved: {output_path} (Pages {start_page}-{end_page})")

    print(f"\n🎉 All lessons split successfully → saved in '{output_dir}' folder.")


if __name__ == "__main__":
    pdf_path = input("Enter main textbook PDF path: ").strip('"')
    lessons = load_lessons()
    split_pdf_by_lessons(pdf_path, lessons)
