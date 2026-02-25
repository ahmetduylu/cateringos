from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # "marketing" veya "chief"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    leads = relationship("Lead", back_populates="assigned_user", foreign_keys="Lead.assigned_user_id")
    logs = relationship("LeadLog", back_populates="user")
