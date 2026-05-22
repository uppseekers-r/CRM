from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import SessionLocal, init_db
from backend.services.student_service import StudentService
from backend.services.task_service import TaskService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

init_db()
app = FastAPI(title="Uppseekers OS Engine API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskCreateSchema(BaseModel):
    student_id: str
    title: str
    description: Optional[str] = None
    priority: str
    deadline: datetime
    assigned_by: str

@app.post("/api/v1/tasks", status_code=status.HTTP_201_CREATED)
def route_create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)):
    try:
        task = TaskService.create_task(
            db=db,
            student_id=payload.student_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            deadline=payload.deadline,
            assigned_by=payload.assigned_by
        )
        return {"status": "success", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/students/{student_id}")
def route_get_student(student_id: str, db: Session = Depends(get_db)):
    student = StudentService.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile records not found")
    return {
        "id": student.id,
        "full_name": student.full_name,
        "gpa": float(student.gpa) if student.gpa else None,
        "sat_score": student.sat_score,
        "total_fee": float(student.total_fee),
        "paid_amount": float(student.paid_amount)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
