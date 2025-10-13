# gamification_module.py
import streamlit as st
from embeddings_utils import get_subjects, load_subject_vector_store

def gamification_page(subject: str, vector_store):
    """
    Gamification UI and logic.
    """
    st.markdown(f"### 🎮 Gamification for {subject}")
    
    # Example: show some mock challenges, points, or badges
    if "gamification_data" not in st.session_state:
        st.session_state.gamification_data = {"points": 0, "badges": []}
    
    data = st.session_state.gamification_data
    
    st.write(f"🏆 Points: {data['points']}")
    st.write(f"🎖 Badges: {', '.join(data['badges']) if data['badges'] else 'None'}")
    
    # Example: simple quiz challenge for gamification
    st.subheader("Quick Challenge!")
    challenge_question = "What is 2 + 2?"
    answer = st.text_input("Answer the challenge question:", key="challenge_input")
    
    if st.button("Submit Challenge Answer"):
        if answer.strip() == "4":
            data["points"] += 10
            data["badges"].append("Math Whiz")
            st.success("✅ Correct! Points and badge awarded.")
        else:
            st.error("❌ Incorrect. Try again!")
import streamlit as st
from embeddings_utils import get_subjects, load_subject_vector_store

st.set_page_config(page_title="Gamification Module")

st.title("🎮 Gamification Module")

# Only for logged in Class 12 students
if st.session_state.get("logged_in") and st.session_state.get("class") == "12":
    subject = st.selectbox("Choose subject for gamification:", get_subjects())
    if subject:
        vector_store = load_subject_vector_store(subject)

        # Your gamification_page logic here
        from gamification_module import gamification_page
        gamification_page(subject, vector_store)

else:
    st.warning("⚠️ Please login as Class 12 student to access gamification.")
