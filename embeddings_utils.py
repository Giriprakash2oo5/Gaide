# embeddings_utils.py
# For loading vector stores and embedding user queries during retrieval using Sentence Transformers

import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import torch


# -----------------------------
# Directories
# -----------------------------
SUBJECTS_DIR = "subjects"
VECTOR_STORE_DIR = "vector_stores"

# -----------------------------
# Initialize embeddings
# -----------------------------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'}  # Force safe load
    )


def get_subjects():
    """Get list of available subjects"""
    if not os.path.exists(SUBJECTS_DIR):
        os.makedirs(SUBJECTS_DIR)
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
    
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=persist_path,
        embedding_function=embeddings
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