import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# -------------------- Config --------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
SUBJECTS_FOLDER = "subjects"
INDEX_BASE_FOLDER = "faiss_indexes"
