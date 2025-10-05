import requests
import streamlit as st

# Load API key from secrets.toml
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_MODEL = "gemini-2.5-flash"

class GeminiLLM:
    def __init__(self, temperature=0.3, model=GEMINI_MODEL):
        self.temperature = temperature
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

    def __call__(self, messages):
        # Collect all user prompts into one string
        user_prompt = " ".join([m.content for m in messages])

        body = {
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {"temperature": self.temperature}
        }

        resp = requests.post(self.endpoint, json=body)
        resp.raise_for_status()
        data = resp.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            st.warning(f"Unexpected Gemini response format: {data}")
            return ""
