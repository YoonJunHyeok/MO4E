from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = 'admin'
    student = 'student'

class MemberBase(BaseModel):
    id: int

class MemberUse(MemberBase):
    name: str
    age: int
    role: Role

class Member(MemberBase):
    name: str
    age: int
    role: Role

    class Config:
        orm_mode = True