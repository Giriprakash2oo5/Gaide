import re
import json
from langchain.schema import HumanMessage

class QuizAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_quiz(self, explanation):
        """Generate quiz from explanation text"""
        prompt = f"""
You are a quiz generator.

Using ONLY the explanation below, create exactly 5 multiple-choice questions.
Return the result STRICTLY in JSON format like this:

[
  {{
    "question": "Who is the author of the poem 'Ulysses'?",
    "options": ["Alfred Tennyson", "Homer", "Shakespeare", "Wordsworth"],
    "correct": "Alfred Tennyson"
  }}
]

Rules:
- Provide exactly 4 options per question.
- "correct" MUST match one of the options exactly.
- Double-check correctness with the explanation.
- Do NOT add explanations or any text outside the JSON array.

EXPLANATION:
{explanation}
"""
        # Use the correct LLM method to get text
        return self.llm.invoke([HumanMessage(content=prompt)])

    def generate_quiz_from_lesson_text(self, lesson_text):
        """Generate quiz from lesson text"""
        prompt = f"""
You are a quiz generator.

Using ONLY the lesson content below, create exactly 5 multiple-choice questions.
Return the result STRICTLY in JSON format like this:

[
  {{
    "question": "Sample Question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": "Option B"
  }}
]

Rules:
- Provide exactly 4 options per question.
- "correct" MUST match one of the options exactly.
- Double-check correctness with the lesson content.
- Do NOT add explanations or any text outside the JSON array.

LESSON CONTENT:
{lesson_text}
"""
        # Use the correct LLM method to get text
        return self.llm.invoke([HumanMessage(content=prompt)])


def parse_quiz(quiz_text):
    """Robust parser for quiz JSON or text output from the LLM."""
    if not quiz_text or not isinstance(quiz_text, str):
        return []

    # Clean up common LLM output artifacts
    quiz_text = quiz_text.strip()
    if quiz_text.startswith("```json"):
        quiz_text = quiz_text[7:]
    elif quiz_text.startswith("```"):
        quiz_text = quiz_text[3:]
    if quiz_text.endswith("```"):
        quiz_text = quiz_text[:-3]
    quiz_text = quiz_text.strip()

    # Try JSON parse first
    try:
        questions = json.loads(quiz_text)
        parsed = []
        for q in questions:
            if all(k in q for k in ["question", "options", "correct"]):
                parsed.append({
                    "q": q["question"],
                    "options": q["options"],
                    "correct": q["correct"]
                })
        if parsed:
            return parsed
    except Exception:
        pass

    # Fallback parser for non-JSON output
    questions = []
    raw_questions = re.split(r'\bQ\d+\s*[:\.]\s*', quiz_text, flags=re.IGNORECASE)[1:]
    if not raw_questions:
        raw_questions = re.split(r'\b\d+\s*[:\.]\s*', quiz_text)[1:]

    for raw_q in raw_questions:
        lines = [ln.strip() for ln in raw_q.strip().split("\n") if ln.strip()]
        if not lines:
            continue

        q_text = lines[0].strip()
        options = []
        correct = None

        for ln in lines[1:]:
            m = re.match(r'^([A-Da-d])[\)\.\:\-]\s*(.+)$', ln.strip())
            if m:
                _, text = m.groups()
                text = text.strip()
                if re.search(r'\(correct\)', text, re.IGNORECASE):
                    clean_text = re.sub(r'\s*\(correct\)\s*', '', text, flags=re.IGNORECASE).strip()
                    correct = clean_text
                    options.append(clean_text)
                else:
                    options.append(text)

        if q_text and len(options) >= 2:
            if not correct:
                correct = options[0]
            questions.append({"q": q_text, "options": options, "correct": correct})

    return questions
