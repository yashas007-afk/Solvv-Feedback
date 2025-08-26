from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from datetime import date, time
from typing import Optional, Annotated

NonEmptyStr255 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
NonEmptyStr100 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
NonEmptyStr2000 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]

class FeedbackBase(BaseModel):
    title: NonEmptyStr255
    client_type: NonEmptyStr100   
    course_name: NonEmptyStr255
    date: date
    client_name: NonEmptyStr255
    questions: NonEmptyStr2000
    time: time

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackPreview(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    title: Optional[NonEmptyStr255] = None
    client_type: Optional[NonEmptyStr100] = None
    course_name: Optional[NonEmptyStr255] = None
    date: Optional[date] = None
    client_name: Optional[NonEmptyStr255] = None
    questions: Optional[NonEmptyStr2000] = None
    time: Optional[time] = None

class FeedbackOut(FeedbackBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
