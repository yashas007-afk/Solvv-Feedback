from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..exceptions import FeedbackNotFoundError

router = APIRouter(tags=["feedback"]) 

@router.post("/feedback/preview", response_model=schemas.FeedbackPreview)
def preview_feedback(feedback: schemas.FeedbackCreate):
    return feedback

@router.post("/feedback/submit", response_model=schemas.FeedbackOut)
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

@router.get("/feedbacks", response_model=List[schemas.FeedbackOut])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(models.Feedback).all()

@router.get("/feedbacks/{feedback_id}", response_model=schemas.FeedbackOut)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise FeedbackNotFoundError(feedback_id)
    return feedback

@router.put("/feedbacks/{feedback_id}", response_model=schemas.FeedbackOut)
def update_feedback(feedback_id: int, updated: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise FeedbackNotFoundError(feedback_id)

    update_data = updated.model_dump(exclude_unset=True, exclude_none=True)
    for field_name, value in update_data.items():
        setattr(db_feedback, field_name, value)

    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise FeedbackNotFoundError(feedback_id)

    db.delete(db_feedback)
    db.commit()
    return {"message": f"Feedback with ID {feedback_id} deleted successfully"}