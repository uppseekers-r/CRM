from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True) # Matches Supabase Auth UID
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False) # super_admin, manager, counselor, mentor, student, parent
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="user")

class StudentProfile(Base):
    __tablename__ = 'students'
    
    id = Column(String, ForeignKey('users.id'), primary_key=True)
    full_name = Column(String, nullable=False)
    parent_email = Column(String)
    phone_number = Column(String)
    grade = Column(String)
    school = Column(String)
    curriculum = Column(String) # IB, CBSE, etc.
    
    # Academics
    gpa = Column(Numeric(4, 2))
    sat_score = Column(Integer)
    ielts_score = Column(Numeric(3, 1))
    
    # University Targets
    dream_universities = Column(JSON, default=[]) # List of strings
    target_universities = Column(JSON, default=[])
    safe_universities = Column(JSON, default=[])
    
    # Workflow
    assigned_counselor_id = Column(String, ForeignKey('users.id'), nullable=True)
    assigned_mentor_id = Column(String, ForeignKey('users.id'), nullable=True)
    package_type = Column(String)
    
    # Finances
    total_fee = Column(Numeric(10, 2), default=0.0)
    paid_amount = Column(Numeric(10, 2), default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="student_profile")
    tasks = relationship("Task", back_populates="student")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String, default="Medium") # Low, Medium, High
    status = Column(String, default="Not Started") # In Progress, Submitted, Under Review, Completed
    deadline = Column(DateTime)
    assigned_by = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("StudentProfile", back_populates="tasks")

class SessionLog(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    counselor_id = Column(String, ForeignKey('users.id'), nullable=False)
    session_date = Column(DateTime, nullable=False)
    meeting_link = Column(String)
    notes = Column(Text)
    action_items = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class DocumentMetadata(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False) # Storage Bucket Key
    document_type = Column(String) # Transcript, SOP, Essay
    uploaded_by = Column(String, ForeignKey('users.id'))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    entity_changed = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")
