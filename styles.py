import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    h1, h2, h3 { text-align: center; }
    .centered-spinner > div { margin: 0 auto !important; }
    .feedback-summary {
      color: #2e7d32;
      font-weight: bold;
      font-size: 20px;
      margin-top: 10px;
      margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
