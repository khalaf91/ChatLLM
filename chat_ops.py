import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st

# Initialize Firebase Admin using secrets
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_CONFIG"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_chat(user_id, chat_id, title, messages):
    doc_ref = db.collection("users").document(user_id).collection("chats").document(chat_id)
    doc_ref.set({
        "title": title,
        "messages": messages,
        "created_at": firestore.SERVER_TIMESTAMP
    }, merge=True)

def list_chats(user_id):
    return db.collection("users").document(user_id).collection("chats").order_by(
        "created_at", direction=firestore.Query.DESCENDING
    ).stream()

def get_chat(user_id, chat_id):
    doc_ref = db.collection("users").document(user_id).collection("chats").document(chat_id)
    return doc_ref.get()

def delete_chat(user_id, chat_id):
    db.collection("users").document(user_id).collection("chats").document(chat_id).delete()
