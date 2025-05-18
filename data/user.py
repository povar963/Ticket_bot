from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from data.db_session import BaseModel
import datetime


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    user_name = Column(String)
    name = Column(String(32))
    hashed_password = Column(String, nullable=False)
    balance = Column(Integer)

    def change_balance(self, value):
        self.balance += value

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
