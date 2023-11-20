import enum
from sqlalchemy import Column, Integer, String, Enum
from db.database import Base

class Role(enum.Enum):
    admin = 'admin'
    student = 'student'

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    role = Column(Enum(Role), nullable=False)