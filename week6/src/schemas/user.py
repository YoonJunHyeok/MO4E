import datetime
from pydantic import BaseModel
from typing import List, Optional

# 요청, 응답의 타입 지정

# user에 기본적으로 들어가야 하는 내용들 - 유저가 입력
class UserBase(BaseModel):
    user_name: str
    age: int

# UserBase를 상속받아서
class UserCreate(UserBase):
    pass

# UserBase를 상속받고, user_id와 created_datetime 추가해서
class User(UserBase):
    user_id: str
    created_datetime: datetime.datetime
    
    class Config:
        orm_mode = True

# 모든 user들
class UserAll(BaseModel):
    total: int # 총 몇 명인지
    users: Optional[List[User]]