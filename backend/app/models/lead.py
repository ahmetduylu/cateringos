from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    isletme_adi = Column(String(255), nullable=False)
    telefon = Column(String(50), index=True)
    adres = Column(Text)
    harita_linki = Column(Text)
    eklenme_tarihi = Column(DateTime(timezone=True), server_default=func.now())
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="havuzda")
    # Olası status değerleri:
    # havuzda | aranmadi_ulasma | gorusuldu_olumlu | teklif_iletildi | kazanildi | ilgilenmiyor

    # İlişkiler
    assigned_user = relationship("User", back_populates="leads", foreign_keys=[assigned_user_id])
    logs = relationship("LeadLog", back_populates="lead", cascade="all, delete-orphan")
