from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import SessionLocal, engine
from models import memberModel

memberModel.Base.metadata.create_all(bind=engine)

memberRouter = APIRouter(
    prefix="/api/v1/members",
    tags=["members"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용자 생성
@memberRouter.post("/", response_model=schemas.Member)
async def createMember(member: schemas.MemberUse, db: Session = Depends(get_db)):
    return crud.createMember(db=db, member=member)

# 전체 사용자 조회
@memberRouter.get("/", response_model=List[schemas.Member])
async def getAllMember(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.getAllMembers(db=db, skip=skip, limit=limit)
    return members

# 특정 아이디 가진 사용자 조회
@memberRouter.get("/{memberId}", response_model=schemas.Member)
async def getOneMember(memberId: int, db: Session = Depends(get_db)):
    member = crud.getOneMember(db, memberId=memberId)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# 특정 아이디 가진 사용자 업데이트
@memberRouter.put("/{memberId}", response_model=schemas.Member)
async def updateMember(memberId: int, updateMember: schemas.MemberUse, db: Session = Depends(get_db)):
    member = crud.getOneMember(db, memberId=memberId)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.updateMember(db=db, memberId=memberId, member=updateMember)

# 특정 아이디 가진 사용자 삭제
@memberRouter.delete("/{memberId}", response_model=schemas.Member)
async def deleteMember(memberId: int, db: Session = Depends(get_db)):
    member = crud.getOneMember(db, memberId=memberId)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.deleteMember(db=db, memberId=memberId)