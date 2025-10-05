# selftest_mode.py
import streamlit as st
from Gaide_learning_platform.agents.quiz_agent import QuizAgent, parse_quiz
from Gaide_learning_platform.agents.feedback_agent import FeedbackAgent

def run_selftest_mode(selected_subject, vector_db, llm):
    """
    Run the Self-Test Mode in Streamlit.
    - Lets user select a lesson
    - Generates a quiz from that lesson
    - Evaluates answers and shows feedback
    """
    st.header(f"🧪 Self-Test Mode: {selected_subject}")

    from embeddings_utils import get_lessons_from_vector_store
    lessons = get_lessons_from_vector_store(vector_db)

    lesson = st.selectbox("Select Lesson", ["--Select--"] + lessons)
    if lesson == "--Select--":
        return

    # Collect lesson chunks
    matched_chunks = []
    for doc in vector_db.docstore._dict.values():
        content = getattr(doc, "page_content", "")
        if lesson.lower() in content.lower():
            matched_chunks.append(content)

    if not matched_chunks:
        st.warning("⚠️ No lesson content found.")
        return

    lesson_text = " ".join(matched_chunks)

    quiz_agent = QuizAgent(llm)
    feedback_agent = FeedbackAgent(llm)

    if st.button("Generate Quiz"):
        with st.spinner("📝 Generating quiz from lesson..."):
            quiz_raw = quiz_agent.generate_quiz_from_lesson_text(lesson_text)
        parsed_quiz = parse_quiz(quiz_raw)

        if not parsed_quiz:
            st.error("⚠️ Failed to parse quiz questions.")
            return

        st.session_state["selftest_quiz"] = parsed_quiz
        st.session_state["selftest_answers"] = [None] * len(parsed_quiz)
        st.session_state["selftest_started"] = True
        st.session_state["selftest_submitted"] = False
        st.session_state["selftest_score"] = 0

    if st.session_state.get("selftest_started", False):
        st.subheader("📋 Quiz Section")
        user_answers = []
        for i, q in enumerate(st.session_state["selftest_quiz"]):
            st.markdown(f"**Q{i+1}. {q['q']}**")
            selected = st.radio(
                "Select answer:",
                options=q["options"],
                key=f"selftest_q{i}",
                horizontal=True,
            )
            user_answers.append(selected)

        if st.button("Submit Answers"):
            st.session_state["selftest_answers"] = user_answers
            score = 0
            st.write("### 📝 Results")

            for i, q in enumerate(st.session_state["selftest_quiz"]):
                user_ans = user_answers[i]
                correct_ans = q.get("correct", "")
                is_correct = (user_ans == correct_ans) and (correct_ans != "")

                if is_correct:
                    score += 1
                    st.markdown(
                        f"**Q{i+1}: {q['q']}**<br>"
                        f"✅ Your Answer: <span style='color:green'>{user_ans}</span><br>"
                        f"✅ Correct Answer: <span style='color:green'>{correct_ans}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    fallback_correct = correct_ans or q.get("correct_letter", "")
                    st.markdown(
                        f"**Q{i+1}: {q['q']}**<br>"
                        f"❌ Your Answer: <span style='color:red'>{user_ans}</span><br>"
                        f"✅ Correct Answer: <span style='color:green'>{fallback_correct}</span>",
                        unsafe_allow_html=True,
                    )

            st.session_state["selftest_score"] = score
            st.session_state["selftest_submitted"] = True
            st.success(
                f"🎯 Final Score: {st.session_state['selftest_score']} / {len(st.session_state['selftest_quiz'])}"
            )

            with st.spinner("📊 Generating feedback..."):
                feedback = feedback_agent.generate_feedback("SELFTEST", user_answers)
            st.markdown("### 🎉 Summary Feedback:")
            st.markdown(
                f'<p class="feedback-summary">{feedback}</p>',
                unsafe_allow_html=True,
            )

