from pydantic import BaseModel
from datetime import date, time

class FeedbackBase(BaseModel):
    title: str
    client_type: str   
    course_name: str
    date: date
    client_name: str
    questions: str
    time: time

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackPreview(FeedbackBase):
    pass

class FeedbackOut(FeedbackBase):
    id: int

    class Config:
        orm_mode = True
