import streamlit as st
from agents.explanation_agent import ExplanationAgent
from agents.quiz_agent import QuizAgent, parse_quiz
from agents.feedback_agent import FeedbackAgent
from llm_utils import GeminiLLM
from embeddings_utils import load_subject_vector_store

def gamification_page(subject, vector_store):
    """
    Gamification Module:
    - Sequential lesson unlock based on quiz score (>=90%).
    - Display lesson cards with progress.
    - Embed quiz per lesson.
    """
    # Initialize LLM and agents
    llm = GeminiLLM()
    expl_agent = ExplanationAgent(llm)
    quiz_agent = QuizAgent(llm)
    feedback_agent = FeedbackAgent(llm)

    # Sample lessons for demo (replace with actual lesson titles from your index)
    lessons = [
        "Ulysses",
        "Prose 1",
        "Prose 2",
        "Poem 1",
        "Poem 2"
    ]

    # Initialize gamification state
    if "gamification_state" not in st.session_state:
        st.session_state.gamification_state = {lesson: {"completed": False, "score": 0} for lesson in lessons}

    st.markdown(f"### 🎓 {subject} Gamification")
    completed_lessons = sum(1 for l in st.session_state.gamification_state.values() if l["completed"])
    st.progress(completed_lessons / len(lessons))

    # Display lesson cards
    col1, col2, col3 = st.columns(3)
    for idx, lesson in enumerate(lessons):
        state = st.session_state.gamification_state[lesson]
        locked = idx > 0 and not st.session_state.gamification_state[lessons[idx - 1]]["completed"]
        card_text = f"{lesson}\n{'✅ Completed' if state['completed'] else '🔒 Locked' if locked else '🎯 Ready'}"
        btn = [col1, col2, col3][idx % 3].button(card_text, key=f"lesson_{idx}", disabled=locked)

        if btn and not locked:
            st.markdown(f"### 📝 Lesson: {lesson}")
            docs = vector_store.similarity_search(lesson, k=5)
            context = "\n".join([d.page_content for d in docs])

            # Show lesson explanation
            st.markdown("#### 📖 Explanation")
            explanation = expl_agent.explain(context, lesson)
            st.write(explanation)

            # Generate Quiz
            st.markdown("#### 🧠 Quiz")
            questions = parse_quiz(quiz_agent.generate_quiz_from_lesson_text(context))
            user_answers = []
            for i, q in enumerate(questions):
                ans = st.radio(f"Q{i+1}: {q['q']}", q["options"], key=f"gam_q_{lesson}_{i}", index=None)
                user_answers.append(ans)

            if st.button("Submit Lesson Quiz", key=f"submit_{lesson}"):
                score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["correct"])
                total = len(questions)
                st.success(f"Score: {score}/{total}")

                # Feedback
                quiz_text = "\n".join([f"Q{i+1}: {q['q']} | Correct: {q.get('correct')}" for i, q in enumerate(questions)])
                feedback = feedback_agent.generate_feedback(quiz_text, user_answers)
                st.markdown("### 💬 Feedback:")
                st.write(feedback)

                # Mark lesson as completed if >=90%
                if score / total >= 0.9:
                    st.session_state.gamification_state[lesson]["completed"] = True
                    st.session_state.gamification_state[lesson]["score"] = score
                    st.success("🎉 Lesson Completed! Next lesson unlocked.")
                else:
                    st.warning("❌ Score less than 90%. Try again to unlock the next lesson.")
