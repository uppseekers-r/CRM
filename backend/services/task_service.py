from sqlalchemy.orm import Session
from backend.models.db_models import Task, AuditLog
from datetime import datetime
from typing import List

class TaskService:
    @staticmethod
    def create_task(db: Session, student_id: str, title: str, description: str, priority: str, deadline: datetime, assigned_by: str) -> Task:
        task = Task(
            student_id=student_id,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            assigned_by=assigned_by,
            status="Not Started"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_student(db: Session, student_id: str) -> List[Task]:
        return db.query(Task).filter(Task.student_id == student_id).order_by(Task.deadline.asc()).all()

    @staticmethod
    def update_task_status(db: Session, task_id: int, status: str, operator_id: str) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = status
            log = AuditLog(user_id=operator_id, action=f"SET_TASK_STATUS_{status.upper()}", entity_changed=str(task_id))
            db.add(log)
            db.commit()
            db.refresh(task)
        return task
