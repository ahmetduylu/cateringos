from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LeadOut(BaseModel):
    id: int
    isletme_adi: str
    telefon: Optional[str] = None
    adres: Optional[str] = None
    harita_linki: Optional[str] = None
    eklenme_tarihi: Optional[datetime] = None
    assigned_user_id: Optional[int] = None
    assigned_user_ad: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class AssignRequest(BaseModel):
    lead_id: int


class StatusUpdateRequest(BaseModel):
    status: str


class NoteAddRequest(BaseModel):
    aciklama: str


class LeadLogOut(BaseModel):
    id: int
    islem_turu: str
    aciklama: Optional[str] = None
    tarih: Optional[datetime] = None
    user_ad: Optional[str] = None

    class Config:
        from_attributes = True


class LeadDetailOut(LeadOut):
    logs: List[LeadLogOut] = []


# Apify'dan gelen ham veri şeması
class ApifyLeadItem(BaseModel):
    title: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None
    website: Optional[str] = None
