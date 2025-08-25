from sqlalchemy import Column, Integer, String, Date, Time
from .database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    client_type = Column(String, nullable=False)   
    course_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    client_name = Column(String, nullable=False)
    questions = Column(String, nullable=False)     
    time = Column(Time, nullable=False)
