from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base() # db가 필요한 곳에 이것 주입


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)