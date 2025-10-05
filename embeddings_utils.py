# embedding_utils.py
# For loading vector stores and embedding user queries during retrieval using Sentence Transformers

import os
import streamlit as st
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load Sentence Transformers Model
# -----------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Use same model as vector store!
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# -----------------------------
# Directories
# -----------------------------
SUBJECTS_DIR = "subjects"
VECTOR_STORE_DIR = "vector_stores"

# -----------------------------
# Embedding Wrapper for Query Embedding
# -----------------------------
class HFEmbeddings:
    def __init__(self):
        # Model already loaded globally
        pass
    
    def embed_query(self, text):
        """Embed a single query text"""
        # SentenceTransformer expects a list, returns a numpy array
        return embedding_model.encode([text])[0].tolist()

# -----------------------------
# Utility Functions
# -----------------------------
def get_subjects():
    if not os.path.exists(SUBJECTS_DIR):
        return []
    return [f for f in os.listdir(SUBJECTS_DIR) if os.path.isdir(os.path.join(SUBJECTS_DIR, f))]


def load_subject_vector_store(subject):
    """Load Chroma vector store for a subject"""
    persist_path = os.path.join(VECTOR_STORE_DIR, subject.lower())
    if not os.path.exists(persist_path):
        raise FileNotFoundError(
            f"❌ Vector store not found for subject '{subject}'. "
            "Run build_vector_stores.py first."
        )
    return Chroma(
        persist_directory=persist_path,
        embedding_function=HFEmbeddings()
    )

def search_subject(subject, query, k=5):
    """Search for relevant documents in a subject"""
    try:
        vector_store = load_subject_vector_store(subject)
        results = vector_store.similarity_search(query, k=k)
        return results
    except Exception as e:
        st.error(f"❌ Error searching {subject}: {str(e)}")
        return []
