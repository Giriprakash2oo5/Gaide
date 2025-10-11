import sys
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass  # Use system sqlite3 if pysqlite3 not available

import streamlit as st
from login_module import init_user_db, user_portal
from embeddings_utils import get_subjects, load_subject_vector_store
from llm_utils import GeminiLLM
from video_module import synthesize_video_from_text,generate_video_from_text
from agents.explanation_agent import ExplanationAgent
from agents.quiz_agent import QuizAgent, parse_quiz
from agents.feedback_agent import FeedbackAgent
from gamification_module import gamification_page  # ✅ Our new module

st.set_page_config(page_title="GAIDE Learning Platform", layout="wide")
st.markdown(
    """
    <style>
        .centered {display: flex; justify-content: center; flex-direction: column; align-items: center;}
        .quiz-box {max-width: 700px; width: 100%; margin:auto;}
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🎓 GAIDE Learning Platform", anchor=None)

init_user_db()


tab1, tab2, tab3 = st.tabs(["Expalanation", "Video Explanation", "Levels of learning"])

# ----------------------------
# Main Content (Learning / Quiz)
# ----------------------------
with tab1:
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first in the sidebar.")
    elif st.session_state.get("class") != "12":
        st.info("📘 Only Class 12 content available.")
    else:
        subject = st.selectbox("Choose subject:", get_subjects())
        if subject:
            vector_store = load_subject_vector_store(subject)
            llm = GeminiLLM()
            expl_agent = ExplanationAgent(llm)
            quiz_agent = QuizAgent(llm)
            feedback_agent = FeedbackAgent(llm)

            mode = st.radio("Mode:", ["Explanation", "Quiz"], horizontal=True)
            prompt = st.text_input("Ask a doubt?/topic:")

            container = st.container()
            with container:
                st.markdown('<div class="centered">', unsafe_allow_html=True)

                if mode == "Explanation" and st.button("Get Explanation") and prompt:
                    docs = vector_store.similarity_search(prompt, k=5)
                    context = "\n".join([d.page_content for d in docs])
                    resp = expl_agent.explain(context, prompt)

                    import re
                    def highlight_text(text):
                        text = re.sub(r'^(#+\s*.*)', r'<span style="color:red; font-weight:bold;">\1</span>', text, flags=re.MULTILINE)
                        text = re.sub(r'\$(.*?)\$', r'<span style="color:red;">\1</span>', text)
                       
                        return text

                    styled_resp = highlight_text(resp)
                    st.markdown("### 📖 Explanation:")
                    st.markdown(styled_resp, unsafe_allow_html=True)
                    

                elif mode == "Quiz":
                    if st.button("Generate Quiz") and prompt:
                        docs = vector_store.similarity_search(prompt, k=5)
                        context = "\n".join([d.page_content for d in docs])
                        questions = parse_quiz(quiz_agent.generate_quiz_from_lesson_text(context))
                        st.session_state.quiz_questions = questions
                        st.session_state.user_answers = []

                    questions = st.session_state.get("quiz_questions", [])
                    if questions:
                        answers = []
                        st.markdown("### 🧠 Answer the following:")
                        for i, q in enumerate(questions):
                            ans = st.radio(f"Q{i+1}: {q['q']}", q["options"], key=f"q_{i}", index=None)
                            answers.append(ans)

                        if st.button("Submit Answers"):
                            score = sum(1 for i, q in enumerate(questions) if answers[i] == q.get("correct"))
                            st.success(f"🎯 Score: {score}/{len(questions)}")

                            quiz_text = "\n".join([f"Q{i+1}: {q['q']} | Correct: {q.get('correct')}" for i, q in enumerate(questions)])
                            feedback = feedback_agent.generate_feedback(quiz_text, answers)
                            st.markdown("### 💬 Feedback:")
                            st.write(feedback)

                            history = st.session_state.get("performance_history", [])
                            history.append({"lesson": prompt, "score": score, "total": len(questions), "attempt": len(history)+1})
                            st.session_state.performance_history = history

                            if len(history) > 1:
                                comp_feedback = feedback_agent.generate_comparative_feedback(
                                    user=st.session_state["username"],
                                    subject=subject,
                                    performance_history=history
                                )
                                st.markdown("### 📊 Comparative Feedback:")
                                st.write(comp_feedback)

                st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Video Generation Tab
# ----------------------------
with tab2:
    st.header("🎥 Generate Video from Explanation")
    user_question = st.text_input("Ask a question to generate explanation video:")

    if st.button("Generate Video") and user_question:
        explanation_agent = ExplanationAgent(llm)
        docs = vector_store.similarity_search(user_question)
        if not docs:
            st.warning("⚠️ No relevant content found in PDFs.")

        context = " ".join([doc.page_content for doc in docs])
        explanation = explanation_agent.explain(context, user_question)
        display_text = getattr(explanation, "content", None)
        if display_text is None and isinstance(explanation, str):
            display_text = explanation

        st.markdown("### 📖 Explanation:")
        st.write(display_text or "")

        # Generate and upload video
        with st.spinner("🎬 Generating video from explanation..."):
            video_url, error = generate_video_from_text(display_text or "")
            if error:
                st.error(f"❌ Video generation failed: {error}")
            elif video_url:
                st.success("✅ Video generated successfully!")
                st.video(video_url)
            else:
                st.warning("⚠️ Video could not be generated.")

# ----------------------------
# Gamification Tab
# ----------------------------
with tab3:
    st.subheader("🎮 Gamification Module")
    if st.session_state.get("logged_in") and st.session_state.get("class") == "12":
        sub = st.selectbox("Choose subject for gamification:", get_subjects(), key="gam_subject")
        if sub:
            vector_store = load_subject_vector_store(sub)
            gamification_page(sub, vector_store)
    else:
        st.warning("⚠️ Please login as Class 12 student to access gamification.")
        
endtime=time.time()
print=endtime-starttime