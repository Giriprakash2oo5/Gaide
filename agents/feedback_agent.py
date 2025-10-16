from langchain.schema import HumanMessage

class FeedbackAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_feedback(self, quiz_text, user_answers):
        answers_str = "\n".join([f"Q{idx+1}: {ans}" for idx, ans in enumerate(user_answers)])
        prompt = f"""
Given the quiz and user answers, provide:
- A short positive summary (use 2-4 gentle emojis).
- Strengths and weaknesses in max 3 sentences.
- If the score is less than 50% then suggest the student to study the concepts again.
Quiz:
{quiz_text}

User answers:
{answers_str}
"""
        return self.llm.invoke([HumanMessage(content=prompt)])

    def generate_comparative_feedback(self, user, subject, performance_history):
        """
        performance_history = [
            {"lesson": "Ulysses", "attempt": 1, "score": 4, "total": 5},
            {"lesson": "Prose 1", "attempt": 1, "score": 2, "total": 5},
            {"lesson": "Prose 1", "attempt": 2, "score": 3, "total": 5},
            ...
        ]
        """
        history_str = "\n".join([
            f"Lesson: {p.get('lesson','Unknown')}, Attempt {p.get('attempt',1)}, "
            f"Score {p.get('score',0)}/{p.get('total',0)}"
            for p in performance_history
        ])

        prompt = f"""
You are an educational feedback coach.

Here is the performance history for student: {user}, subject: {subject}:

{history_str}

Please give comparative feedback:
- Mention which lessons they are doing better in compared to others.
- Highlight areas where they are weaker and suggest to study the concepts again.
- Encourage improvement with supportive language.
- Keep it short (3-4 sentences).
"""
        return self.llm.invoke([HumanMessage(content=prompt)])
