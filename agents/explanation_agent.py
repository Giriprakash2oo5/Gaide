
class ExplanationAgent:
    def __init__(self, llm):
        self.llm = llm

    def explain(self, context, question):
        prompt = f"""
-Answer the question based on the PDF with additional .
-If there is a image attached to the explanation then you must generate the image exactly given in the context.

If not found, give some definition and say:
"Wow you are asking from out of syllabus. Just go on with it, but don't go deeply!"

CONTEXT:
{context}

QUESTION:
{question}

Detailed answer:
"""
        return self.llm.invoke(prompt)
