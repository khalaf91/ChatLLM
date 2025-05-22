import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase config from Streamlit secrets
firebase_config = dict(st.secrets["FIREBASE_CONFIG"])

# Fix private_key newlines if escaped
if "\\n" in firebase_config["private_key"]:
    firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_chat(user_id, chat_id, title, messages):
    """Save or update a chat document for the given user."""
    doc_ref = db.collection("users").document(user_id).collection("chats").document(chat_id)
    doc_ref.set({
        "title": title,
        "messages": messages,
        "created_at": firestore.SERVER_TIMESTAMP
    }, merge=True)

def list_chats(user_id):
    """Return a list of chat documents ordered by creation time descending."""
    chats = db.collection("users").document(user_id).collection("chats") \
        .order_by("created_at", direction=firestore.Query.DESCENDING).stream()
    return chats

def get_chat(user_id, chat_id):
    """Retrieve a single chat document for a user."""
    doc_ref = db.collection("users").document(user_id).collection("chats").document(chat_id)
    return doc_ref.get()

def delete_chat(user_id, chat_id):
    """Delete a chat document."""
    db.collection("users").document(user_id).collection("chats").document(chat_id).delete()
