import streamlit as st
from chatbot.auth import create_user_table, signup_user, login_user
from chatbot.bot import ask_bot, response_scores
from chatbot.database import init_db, log_conversation, get_user_history

# Initialize DB and User Table
init_db()
create_user_table()

# Streamlit UI config
st.set_page_config(page_title="Affiliate Creatives Educator Bot", layout="centered")
st.title("🎯 Affiliate Creatives Educator Bot")

# Session handling
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login / Signup Tabs
def login_signup():
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")

    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        if st.button("Signup"):
            try:
                signup_user(new_user, new_pass)
                st.success("✅ User created! You can login now.")
            except:
                st.error("⚠️ Username already exists.")

# If not logged in, show auth UI
if not st.session_state.authenticated:
    login_signup()

# If logged in, show chat interface
else:
    st.subheader("💬 Ask about *creatives in affiliate marketing*")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Type your question:")

    if user_input:
        response = ask_bot(user_input)
        st.session_state.chat.append((user_input, response))
        log_conversation(st.session_state.username, user_input, response, feedback="none")

    # Chat display with feedback buttons
    for i, (msg, res) in enumerate(reversed(st.session_state.chat)):
        with st.container():
            st.markdown(f"**🧑 You:** {msg}")
            st.markdown(f"**🤖 Bot:** {res}")
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                if st.button("👍", key=f"up_{i}"):
                    response_scores[msg] = response_scores.get(msg, 0) + 1
                    log_conversation(st.session_state.username, msg, res, feedback="up")
                    st.success("Feedback recorded 👍")

            with col2:
                if st.button("👎", key=f"down_{i}"):
                    response_scores[msg] = response_scores.get(msg, 0) - 1
                    log_conversation(st.session_state.username, msg, res, feedback="down")
                    st.warning("Feedback recorded 👎")

            with col3:
                score = response_scores.get(msg, 0)
                st.write(f"🔁 RL Score: `{score}`")

    # Chat history section
    with st.expander("📜 View Your Chat History"):
        history = get_user_history(st.session_state.username)
        for msg, res, fb, ts in reversed(history):
            st.markdown(f"🕒 `{ts}`")
            st.markdown(f"- **You:** {msg}")
            st.markdown(f"- **Bot:** {res}")
            st.markdown(f"- **Feedback:** {fb}")
            st.markdown("---")
