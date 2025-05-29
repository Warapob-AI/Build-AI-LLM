from services.database.user_database_controller import create_database, insert_user, delete_user, get_user
from dotenv import load_dotenv

import streamlit as st
import os

load_dotenv()

if "username" not in st.session_state:
    st.session_state.username = None

if "password" not in st.session_state:
    st.session_state.password = None