import streamlit as st
import os
from dotenv import load_dotenv
from database import init_db
from customer_view import show_customer_view
from seller_view import show_seller_view

load_dotenv()

SELLER_PASSWORD = os.getenv("SELLER_PASSWORD", "admin123")

init_db()

st.set_page_config(page_title="COD Order Manager", page_icon="📦", layout="wide")

if "is_seller" not in st.session_state:
    st.session_state.is_seller = False

# Sidebar: mode switch
with st.sidebar:
    st.header("Navigation")
    mode = st.radio("I am a:", ["Customer", "Seller (Admin)"])

if mode == "Customer":
    st.session_state.is_seller = False
    show_customer_view()

else:
    if not st.session_state.is_seller:
        st.title("🔐 Seller Login")
        password_input = st.text_input("Enter seller password", type="password")
        if st.button("Login"):
            if password_input == SELLER_PASSWORD:
                st.session_state.is_seller = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    else:
        show_seller_view()
        if st.button("Log out"):
            st.session_state.is_seller = False
            st.rerun()