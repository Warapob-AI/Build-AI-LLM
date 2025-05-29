from services.database.user_database_controller import get_user, insert_user, create_database, get_user_pass
from streamlit_extras.stylable_container import stylable_container
from pages.chat_ai_text import chat_ai_text
from dotenv import load_dotenv

import streamlit as st 
import time 
import os

load_dotenv()

def login():
    st.title("ระบบเข้าสู่ระบบผู้ใช้")

    if st.session_state.username is None or st.session_state.password is None:
        st.warning("กรุณากรอกข้อมูลเข้าสู่ระบบเพื่อพูดคุยกับระบบแชท AI ของเรา")


    username = st.text_input("ชื่อผู้ใช้", key="username_input")
    password = st.text_input("รหัสผ่าน", type="password", key="password_input")

    if username and password:
        st.session_state.username = username
        st.session_state.password = password
    if not username or not password: 
        st.session_state.username = None
        st.session_state.password = None

    col_left, col_right = st.columns([1, 1])

    with col_left:
        login_button = st.button("เข้าสู่ระบบ", key="login_button")
    
    with col_right:
        with stylable_container(
            key="register_button",
            css_styles="""
            button{
                float: right;
            }
            """
            ):
            register_button = st.button("ยังไม่มีบัญชีเข้าระบบ?", key="register_button")

    if login_button:
        if len(username) < 4 and len(username) > 30:
            st.error("ชื่อผู้ใช้ต้องมีความยาวระหว่าง 4 ถึง 30 ตัวอักษร")
            return
        
        elif len(password) < 8 and len(password) > 30:
            st.error("รหัสผ่านต้องมีความยาวระหว่าง 8 ถึง 30 ตัวอักษร")
            return
        
        elif (not get_user_pass(username, password)):
            st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่")
            return
        else:
            st.success(f"ยินดีต้อนรับ {username}! ระบบกำลังนำคุณไปยังหน้าแชท AI")
            time.sleep(2)  # รอสักครู่ก่อนเปลี่ยนหน้า
            st.session_state.menu_mode = "chat_mode"
            st.rerun()



    if register_button:
        st.session_state.menu_mode = "register_mode"
        st.rerun()

def register():
    st.title("ระบบลงทะเบียนผู้ใช้")

    if "new_username" not in st.session_state:
        st.session_state.new_username = None

    if "new_password" not in st.session_state:
        st.session_state.new_password = None

    if "new_confirm_password" not in st.session_state:
        st.session_state.new_confirm_password = None

    if st.session_state.new_username is None or st.session_state.new_password is None:
        st.warning("กรุณากรอกข้อมูลลงทะเบียนเพื่อเข้าสู่ระบบแชท AI ของเรา")

    new_username = st.text_input("ชื่อผู้ใช้ใหม่", key="new_username_input")
    new_password = st.text_input("รหัสผ่านใหม่", type="password", key="new_password_input")
    new_confirm_password = st.text_input("ยืนยันรหัสผ่านใหม่", type="password", key="new_confirm_password_input")

    if new_username and new_password:
        st.session_state.new_username = new_username
        st.session_state.new_password = new_password
        st.session_state.new_confirm_password = new_confirm_password

    if not new_username or not new_password or not new_confirm_password: 
        st.session_state.new_username = None
        st.session_state.new_password = None
        st.session_state.new_confirm_password = None

    register_button = st.button("ลงทะเบียน", key="register_button")

    if register_button:
        if len(new_username) < 4 and len(new_username) > 30:
            st.error("ชื่อผู้ใช้ต้องมีความยาวระหว่าง 4 ถึง 30 ตัวอักษร")
            return
        
        elif len(new_password) < 8 and len(new_password) > 30:
            st.error("รหัสผ่านต้องมีความยาวระหว่าง 8 ถึง 30 ตัวอักษร")
            return
        
        elif new_password != new_confirm_password:
            st.error("รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่")
            return
        
        else:
            if get_user(new_username):
                st.error(f"ชื่อผู้ใช้ {new_username} ถูกใช้งานแล้ว กรุณาเลือกชื่อผู้ใช้อื่น")
                return
            else:
                insert_user(new_username, new_password)
                st.success(f"ลงทะเบียนสำเร็จ! ระบบกำลังนำคุณไปยังหน้าเข้าสู่ระบบ")
                time.sleep(2)  
                st.session_state.menu_mode = "login_mode"
                st.rerun()
                
                # รอสักครู่ก่อนเปลี่ยนหน้า

if "menu_mode" not in st.session_state:
    st.session_state.menu_mode = "login_mode"

if st.session_state.menu_mode == "login_mode":
    login()

if st.session_state.menu_mode == "register_mode":
    register()

if st.session_state.menu_mode == "chat_mode" and st.session_state.username:
    st.switch_page("pages/chat_ai_text.py")
    st.rerun()
