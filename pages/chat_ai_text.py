from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

load_dotenv()
import pytz
import os

from services.database.chat_text_database_controller import get_recent_chat_history, insert_chat_history
from api.gemini.chat_text_gemini_controller import chat_with_ai, chat_header_ai_gen
from streamlit_extras.stylable_container import stylable_container

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_thai_timestamp():
    tz = pytz.timezone('Asia/Bangkok')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

with st.sidebar:
    st.header("ตั้งค่า Gemini API Key")
    api_key_input = st.text_input("🔑 Gemini API Key", value=os.getenv('GEMINI_API_KEY', ''), type="password")
    if api_key_input:
        st.session_state.gemini_api_key = api_key_input
    else:
        st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY')

def chat_ai_text():
    new_chat_button = None
    chat_response = None
    chat_header = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_header" not in st.session_state: 
        st.session_state.chat_header = None

    new_chat_button = st.button("New Chat!", key = "new_chat_button")

    with open("prompts/chatAIText.txt", "r", encoding="utf-8") as file:
        chatAIText = file.read()

    introduceText = f"สวัสดี คุณ {st.session_state.username}! ยินดีต้อนรับสู่ระบบแชท AI ของเรา"

    with st.chat_message("assistant"):
        st.success(introduceText)

    # ส่วนรับข้อความแบบ chat_input
    user_input = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")
    
    if user_input:
        # บันทึกข้อความของผู้ใช้ในประวัติการแชท
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # ประมวลผลข้อความของผู้ใช้และส่งไปยัง AI
        with st.spinner("Gemini กำลังตอบ..."):
            # สร้าง header สำหรับข้อความ AI
            chat_header = None 

            if st.session_state.chat_header is None: 
                print("")
                chat_header = chat_header_ai_gen(user_input, st.session_state.gemini_api_key)
                st.session_state.chat_header = chat_header

            # ในฟังก์ชันที่คุยกับ AI
            history = get_recent_chat_history(st.session_state.username, st.session_state.chat_header)

            # สร้าง prompt ที่รวมประวัติ
            history_prompt = ""
            for row in history:
                history_prompt += f"User: {row[1]}\nAssistant: {row[2]}\n"

            # เพิ่มข้อความใหม่
            full_prompt = history_prompt + f"User: {user_input}\nAssistant:"

            # ส่ง full_prompt ไปยัง LLM
            chat_response = chat_with_ai(full_prompt, st.session_state.gemini_api_key)

        # บันทึกข้อความตอบกลับจาก AI ในประวัติการแชท
        st.session_state.chat_history.append({"role": "assistant", "content": chat_response})

    print(st.session_state.chat_header)
    
    # แสดงประวัติการแชท
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.info(chat["content"])
        else:
            with st.chat_message("assistant"):
                st.success(chat["content"])


    if user_input and chat_response and st.session_state.chat_header:
        insert_chat_history(
            st.session_state.username,
            user_input,
            chat_response,
            st.session_state.chat_header,
            get_thai_timestamp()
        )

    if new_chat_button:
        st.session_state.chat_history = []
        st.session_state.chat_header = []
        st.rerun()

if st.session_state.username is None: 
    st.error("ยังไม่ได้เข้าสู่ระบบ โปรดเข้าสู่ระบบ!")
    st.stop()


chat_ai_text()