import streamlit as st
import plotly.express as px
import pandas as pd
from backend.database.connection import SessionLocal
from backend.models.db_models import StudentProfile, Task

def render_admin():
    st.title("⚙️ Super Admin Control Workspace")
    
    # Query database live state parameters across engine metrics execution spaces
    db = SessionLocal()
    students = db.query(StudentProfile).all()
    tasks = db.query(Task).all()
    db.close()
    
    # Mathematical data normalization layer pipelines
    total_students = len(students)
    total_rev = sum([float(s.total_fee) for s in students]) if students else 0.0
    collected_rev = sum([float(s.paid_amount) for s in students]) if students else 0.0
    pending_rev = total_rev - collected_rev
    
    # KPI Grid Dashboard UI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Active Lifecycle Records", total_students)
    with col2:
        st.metric("Gross Pipeline Value Booked", f"${total_rev:,.2f}")
    with col3:
        st.metric("Collected Working Capital", f"${collected_rev:,.2f}", delta=f"{((collected_rev/total_rev)*100 if total_rev > 0 else 0):.1f}% Collections")
    with col4:
        st.metric("Outstanding Accounts Receivable", f"${pending_rev:,.2f}", delta_color="inverse")
        
    st.markdown("---")
    
    # Interactive Data Representation Space utilizing Plotly analytical components
    st.subheader("Pipeline Realization & Conversion Analytics")
    if students:
        chart_df = pd.DataFrame([{
            'Student': s.full_name,
            'Committed': float(s.total_fee),
            'Realized': float(s.paid_amount)
        } for s in students])
        
        fig = px.bar(chart_df, x='Student', y=['Committed', 'Realized'], 
                     title="Contract Breakdown Context Analysis Profile", barmode='group',
                     color_discrete_sequence=['#1E3A8A', '#3B82F6'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactional students running inside system pipelines at present.")
