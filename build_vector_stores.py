# build_vector_stores.py
# For creating and storing document embeddings in Chroma using HuggingFace Sentence Transformers

import os
import PyPDF2
from pathlib import Path
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
import torch

# Directories
VECTOR_STORE_DIR = Path("vector_stores")
SUBJECTS_DIR = Path("subjects")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Make sure same everywhere!

# --------------------------
# CHANGED PORTION: Embeddings class
# --------------------------
class HFEmbeddings:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

# --------------------------
# PDF Text Extraction
# --------------------------
def extract_pdf_text(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
    return text

# --------------------------
# Chunking Function
# --------------------------
def simple_chunking(text, max_length=250):
    raw_chunks = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    for chunk in raw_chunks:
        while len(chunk.split()) > max_length:
            words = chunk.split()
            chunks.append(' '.join(words[:max_length]))
            chunk = ' '.join(words[max_length:])
        if chunk:
            chunks.append(chunk)
    return chunks

def get_subjects():
    if not SUBJECTS_DIR.exists():
        return []
    return [f.name for f in SUBJECTS_DIR.iterdir() if f.is_dir()]

def build_vector_store(subject):
    subject_path = SUBJECTS_DIR / subject
    if not subject_path.exists():
        print(f"❌ Subject folder not found: {subject}")
        return

    docs = []
    pdf_files = list(subject_path.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {subject_path}")
        return

    print(f"📚 Processing {len(pdf_files)} PDF files for subject: {subject}")

    for file in pdf_files:
        print(f"  📄 Processing: {file.name}")
        text = extract_pdf_text(file)
        if text.strip():
            chunks = simple_chunking(text, max_length=250)
            for idx, chunk in enumerate(chunks):
                docs.append(Document(
                    page_content=chunk,
                    metadata={"source": str(file), "subject": subject, "chunk_id": idx}
                ))
        else:
            print(f"  ⚠️  No text extracted from {file.name}")

    if not docs:
        print(f"❌ No valid documents found for subject: {subject}")
        return

    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embedding_function = HFEmbeddings(embedding_model)  # <-- CHANGED PORTION

    persist_path = VECTOR_STORE_DIR / subject.lower()
    persist_path.mkdir(parents=True, exist_ok=True)

    print(f"🔄 Creating vector store with {len(docs)} chunks...")
    vector_store = Chroma(
        persist_directory=str(persist_path),
        embedding_function=embedding_function  # <-- CHANGED PORTION
    )
    vector_store.add_documents(docs)
    print(f"✅ Vector store created for subject: {subject}")

def main():
    subjects = get_subjects()
    if not subjects:
        print("❌ No subjects found in the subjects folder.")
        return

    print(f"🚀 Found {len(subjects)} subjects: {', '.join(subjects)}")

    for subject in subjects:
        print(f"\n📖 Building vector store for: {subject}")
        build_vector_store(subject)

if __name__ == "__main__":
    main()
