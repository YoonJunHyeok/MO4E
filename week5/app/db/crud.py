from sqlalchemy.orm import Session
from . import schemas
from models.memberModel import Member

def getOneMember(db: Session, memberId: int):
    return db.query(Member).filter(Member.id == memberId).first()

def getAllMembers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()

def createMember(db: Session, member: schemas.MemberUse):
    db_member = Member(name=member.name, age=member.age, role=member.role)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def updateMember(db: Session, memberId: int, member: schemas.MemberUse):
    db_member = getOneMember(db, memberId)

    if(member.name): 
        db_member.name = member.name
    if(member.age): 
        db_member.age = member.age
    if(member.role): 
        db_member.role = member.role

    db.commit()
    db.refresh(db_member)
    print(db_member.role)
    return db_member

def deleteMember(db: Session, memberId: int):
    db_member = getOneMember(db, memberId)
    db.delete(db_member)
    db.commit()
    return db_member