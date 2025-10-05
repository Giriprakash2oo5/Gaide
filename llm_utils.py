# llm_utils.py

import os
import google.generativeai as genai

class GeminiLLM:
    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY environment variable not set. Please set it before running the app.")
        genai.configure(api_key=api_key)

        # Correct way to load Gemini model
        self.model = genai.GenerativeModel(model_name)

    def query(self, prompt: str, vector_store=None, k: int = 3):
        """
        Query Gemini LLM, optionally providing context from a vector store (for RAG).
        """
        context = ""
        if vector_store is not None:
            try:
                docs = vector_store.similarity_search(prompt, k=k)
                context = "\n\n".join(doc.page_content for doc in docs)
            except Exception as e:
                context = ""
                print(f"Warning: RAG context could not be retrieved. {str(e)}")

        full_prompt = f"""
You are a subject expert teacher.

Context from textbooks:
{context}

Question: {prompt}

Answer in detail with explanations that are suitable for a student.
"""

        # Generate response
        try:
            response = self.model.generate_content(full_prompt)
            return getattr(response, "text", str(response))
        except Exception as e:
            return f"❌ Gemini API Error: {str(e)}"

    # For compatibility with agents expecting `.invoke(prompt)`
    def invoke(self, prompt: str):
        return self.query(prompt)
