import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.db_models import Task, StudentProfile
from backend.services.task_service import TaskService

def render_student():
    st.title("🎓 Student Achievement Engine Portal Workspace")
    sid = st.session_state.user_id
    
    db = SessionLocal()
    profile = db.query(StudentProfile).filter(StudentProfile.id == sid).first()
    my_tasks = db.query(Task).filter(Task.student_id == sid).all()
    db.close()
    
    if profile:
        st.write(f"### Welcome back, :blue[{profile.full_name}]")
        
    st.subheader("Your Roadmap Actions Tasks Queue Tracking Index")
    if not my_tasks:
        st.info("No actionable directives outstanding in your queue environment.")
        return
        
    for task in my_tasks:
        with st.expander(f"[{task.priority.upper()}] {task.title} — Status: **{task.status}**"):
            st.write(task.description)
            st.caption(f"Deadline Frame: {task.deadline}")
            
            if task.status != "Completed":
                if st.button("Mark Assignment Checklist Item as Resolved", key=f"btn_tsk_{task.id}"):
                    db_session = SessionLocal()
                    TaskService.update_task_status(db_session, task.id, "Completed", sid)
                    db_session.close()
                    st.success("Status flag modified successfully.")
                    st.rerun()
