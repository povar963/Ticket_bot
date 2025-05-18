from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, TIME
from data.db_session import BaseModel


class Event_model(BaseModel):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cost = Column(Integer)
    date_time = Column(String)
    name = Column(String(16))
    type = Column(String(16))
    description = Column(String(256))
    author_id = Column(String)
    author_user_id = Column(String)
    users = Column(Integer)

