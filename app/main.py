from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Feedback Service")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/feedback/preview", response_model=schemas.FeedbackPreview)
def preview_feedback(feedback: schemas.FeedbackCreate):
    return feedback

@app.post("/feedback/submit", response_model=schemas.FeedbackOut)
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(
        title=feedback.title,
        client_type=feedback.client_type,
        course_name=feedback.course_name,
        date=feedback.date,
        client_name=feedback.client_name,
        questions=feedback.questions,
        time=feedback.time,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/feedbacks", response_model=List[schemas.FeedbackOut])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(models.Feedback).all()

@app.get("/feedbacks/{feedback_id}", response_model=schemas.FeedbackOut)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail=f"Feedback with ID {feedback_id} not found")
    return feedback

@app.put("/feedbacks/{feedback_id}", response_model=schemas.FeedbackOut)
def update_feedback(feedback_id: int, updated: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail=f"Feedback with ID {feedback_id} not found")

    db_feedback.title = updated.title
    db_feedback.client_type = updated.client_type
    db_feedback.course_name = updated.course_name
    db_feedback.date = updated.date
    db_feedback.client_name = updated.client_name
    db_feedback.questions = updated.questions
    db_feedback.time = updated.time

    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@app.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail=f"Feedback with ID {feedback_id} not found")

    db.delete(db_feedback)
    db.commit()
    return {"message": f"Feedback with ID {feedback_id} deleted successfully"}
