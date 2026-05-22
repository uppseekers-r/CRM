import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
# ... leave the rest of your file exactly the same
import streamlit as st
from backend.auth.supabase_auth import AuthenticationManager
from backend.database.connection import SessionLocal
from backend.models.db_models import User

# Pages Router Imports
from pages.admin_dashboard import render_admin
from pages.manager_dashboard import render_manager
from pages.counselor_dashboard import render_counselor
from pages.student_dashboard import render_student

st.set_page_config(page_title="Uppseekers OS", layout="wide", initial_sidebar_state="expanded")

auth_mgr = AuthenticationManager()

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_id = None
    st.session_state.user_role = None
    st.session_state.user_email = None

def fetch_local_role(uid: str) -> str:
    db = SessionLocal()
    user_record = db.query(User).filter(User.id == uid).first()
    db.close()
    return user_record.role if user_record else "student"

# Auth View
if not st.session_state.user_authenticated:
    st.title("Uppseekers OS")
    st.subheader("Internal Student Journey Management Platform")
    
    with st.form("Login Form"):
        email = st.text_input("Corporate Email Address")
        password = st.text_input("Security Access Password", type="password")
        submitted = st.form_submit_button("Authenticate into Workstation")
        
        if submitted:
            res = auth_mgr.login_user(email, password)
            if res and res.user:
                st.session_state.user_authenticated = True
                st.session_state.user_id = res.user.id
                st.session_state.user_email = res.user.email
                st.session_state.user_role = fetch_local_role(res.user.id)
                st.success("Authorization Verified.")
                st.rerun()
            else:
                st.error("Invalid corporate identity credentials.")
else:
    # Sidebar Navigation Context Framework
    st.sidebar.title("Uppseekers OS")
    st.sidebar.write(f"**Identity:** {st.session_state.user_email}")
    st.sidebar.write(f"**Role Engine:** :blue[{st.session_state.user_role.upper()}]")
    
    if st.sidebar.button("Terminate Session", use_container_width=True):
        st.session_state.user_authenticated = False
        st.rerun()
        
    # Multi-Route Processing Pipeline Based on Access Scope Controls
    role = st.session_state.user_role
    if role == "super_admin":
        render_admin()
    elif role == "manager":
        render_manager()
    elif role == "counselor":
        render_counselor()
    elif role == "student":
        render_student()
    else:
        st.error("Role provisioning context mismatch error.")
