from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class LeadLog(Base):
    __tablename__ = "lead_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    islem_turu = Column(String(50), nullable=False)
    # islem_turu: "not_eklendi" | "durum_degisti" | "atandi" | "apify_import"
    aciklama = Column(Text)
    tarih = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    lead = relationship("Lead", back_populates="logs")
    user = relationship("User", back_populates="logs")
