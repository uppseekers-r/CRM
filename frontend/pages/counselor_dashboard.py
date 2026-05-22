import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.db_models import StudentProfile, Task
from backend.services.task_service import TaskService
from datetime import datetime

def render_counselor():
    st.title("📋 Counselor Allocation Station")
    cid = st.session_state.user_id
    
    db = SessionLocal()
    my_students = db.query(StudentProfile).filter(StudentProfile.assigned_counselor_id == cid).all()
    db.close()
    
    st.subheader("Assigned Account Assets")
    if not my_students:
        st.info("No case accounts assigned to this profile context.")
        return
        
    student_mapping = {s.full_name: s.id for s in my_students}
    selected_student_name = st.selectbox("Select Student Lifecycle Context", list(student_mapping.keys()))
    target_student_id = student_mapping[selected_student_name]
    
    st.markdown("### Operational Actions Frame")
    tab1, tab2 = st.tabs(["Task Assignment Processing", "Profile Roadmap Status Check"])
    
    with tab1:
        with st.form("Task Generator Engine Pipeline"):
            title = st.text_input("Task Objective Context Title")
            desc = st.text_area("Detailed Directives Instruction Payload")
            priority = st.selectbox("Urgency Weight Matrix Indicator", ["Low", "Medium", "High"])
            deadline_date = st.date_input("Target Resolution Date Threshold")
            
            if st.form_submit_button("Publish Task to Student Pipeline"):
                db_session = SessionLocal()
                TaskService.create_task(
                    db=db_session,
                    student_id=target_student_id,
                    title=title,
                    description=desc,
                    priority=priority,
                    deadline=datetime.combine(deadline_date, datetime.min.time()),
                    assigned_by=cid
                )
                db_session.close()
                st.success(f"Task broadcasted to {selected_student_name} processing pipelines.")
