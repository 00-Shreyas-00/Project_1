from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr
from app.services.db_service import Base

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    google_id = Column(String, unique=True, index=True, nullable=True)

# Pydantic Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    google_id: str | None = None

    class Config:
        from_attributes = True
