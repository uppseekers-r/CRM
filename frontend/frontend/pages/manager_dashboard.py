import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.db_models import StudentProfile

def render_manager():
    st.title("💼 Management Allocation Desk")
    
    db = SessionLocal()
    students = db.query(StudentProfile).all()
    db.close()
    
    st.subheader("Global Student Registry")
    if students:
        summary_data = [{
            "Name ID Key": s.id,
            "Full Student Identity": s.full_name,
            "Current Curriculum Layout": s.curriculum,
            "Assigned Counselor Token": s.assigned_counselor_id if s.assigned_counselor_id else "Unassigned Pool"
        } for s in students]
        st.dataframe(summary_data, use_container_width=True)
    else:
        st.warning("No tracked global profile indexes found inside records pools.")
