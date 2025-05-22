import streamlit as st
import openai
from firebase_admin import auth
from chat_ops import save_chat, list_chats, get_chat, delete_chat
from uuid import uuid4

st.set_page_config(page_title="ChatLLM by Mr. K", layout="wide")

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Sidebar Login Interface ---
st.sidebar.title("🔐 User Login")
st.sidebar.markdown("1. [Open Login Page](firebase_login.html) and sign in with Google.")
token_input = st.sidebar.text_area("2. Paste Firebase ID Token here:", height=100)
verify_button = st.sidebar.button("✅ Verify Token")

user_email = None
user_id = None

if verify_button and token_input:
    try:
        decoded_token = auth.verify_id_token(token_input)
        user_email = decoded_token.get("email")
        user_id = decoded_token.get("uid")
        st.sidebar.success(f"✅ Logged in as: {user_email}")
    except Exception as e:
        st.sidebar.error(f"❌ Token verification failed: {str(e)}")

# --- Main Chat Interface ---
if user_id:
    st.title("💬 ChatLLM by Mr. K")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask anything...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Save chat session
        chat_id = "chat_" + str(uuid4())[:8]
        save_chat(user_id, chat_id, title="Chat Session", messages=st.session_state.messages)

else:
    st.warning("⚠️ Please log in with your Google account to use ChatLLM.")
