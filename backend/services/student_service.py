from sqlalchemy.orm import Session
from backend.models.db_models import StudentProfile, User, AuditLog
from typing import List, Dict, Any

class StudentService:
    @staticmethod
    def get_all_students(db: Session) -> List[StudentProfile]:
        return db.query(StudentProfile).all()
    
    @staticmethod
    def get_student_by_id(db: Session, student_id: str) -> StudentProfile:
        return db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    
    @staticmethod
    def create_student_profile(db: Session, profile_data: Dict[str, Any], operator_id: str) -> StudentProfile:
        # Create shadow table user entity inside metadata index tracking first
        new_user = User(id=profile_data['id'], email=profile_data['email'], role='student')
        db.add(new_user)
        db.flush()
        
        new_profile = StudentProfile(
            id=profile_data['id'],
            full_name=profile_data['full_name'],
            parent_email=profile_data.get('parent_email'),
            phone_number=profile_data.get('phone_number'),
            grade=profile_data.get('grade'),
            school=profile_data.get('school'),
            curriculum=profile_data.get('curriculum'),
            package_type=profile_data.get('package_type'),
            total_fee=profile_data.get('total_fee', 0.0),
            assigned_counselor_id=profile_data.get('assigned_counselor_id')
        )
        db.add(new_profile)
        
        log = AuditLog(user_id=operator_id, action="CREATE_STUDENT_PROFILE", entity_changed=profile_data['id'])
        db.add(log)
        
        db.commit()
        return new_profile

    @staticmethod
    def update_student_metrics(db: Session, student_id: str, updates: Dict[str, Any], operator_id: str) -> StudentProfile:
        profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if profile:
            for key, value in updates.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            log = AuditLog(user_id=operator_id, action="UPDATE_STUDENT_METRICS", entity_changed=student_id)
            db.add(log)
            db.commit()
        return profile
