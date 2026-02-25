from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.deps import get_current_user
from app.database import get_db
from app.models.lead import Lead
from app.models.lead_log import LeadLog
from app.models.user import User
from app.schemas.lead import (
    LeadOut,
    LeadDetailOut,
    LeadLogOut,
    AssignRequest,
    StatusUpdateRequest,
    NoteAddRequest,
)

router = APIRouter(prefix="/leads", tags=["Leads"])

VALID_STATUSES = [
    "havuzda",
    "aranmadi_ulasma",
    "gorusuldu_olumlu",
    "teklif_iletildi",
    "kazanildi",
    "ilgilenmiyor",
]


def _lead_to_out(lead: Lead) -> LeadOut:
    return LeadOut(
        id=lead.id,
        isletme_adi=lead.isletme_adi,
        telefon=lead.telefon,
        adres=lead.adres,
        harita_linki=lead.harita_linki,
        eklenme_tarihi=lead.eklenme_tarihi,
        assigned_user_id=lead.assigned_user_id,
        assigned_user_ad=lead.assigned_user.ad if lead.assigned_user else None,
        status=lead.status,
    )


@router.get("/pool", response_model=list[LeadOut])
def get_pool(
    search: str = "",
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Havuzdaki (atanmamış) müşterileri listele."""
    query = db.query(Lead).filter(Lead.assigned_user_id.is_(None))
    if search:
        query = query.filter(
            Lead.isletme_adi.ilike(f"%{search}%")
            | Lead.telefon.ilike(f"%{search}%")
            | Lead.adres.ilike(f"%{search}%")
        )
    leads = query.order_by(Lead.eklenme_tarihi.desc()).offset(skip).limit(limit).all()
    return [_lead_to_out(l) for l in leads]


@router.post("/assign", response_model=LeadOut)
def assign_lead(
    body: AssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Müşteriyi mevcut kullanıcıya ata.
    SELECT FOR UPDATE ile row-level lock — aynı anda iki kişi alamaz.
    """
    # Row-level lock ile al
    lead = (
        db.query(Lead)
        .filter(Lead.id == body.lead_id)
        .with_for_update()
        .first()
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    if lead.assigned_user_id is not None:
        raise HTTPException(
            status_code=409,
            detail="Bu müşteri zaten başka bir personele atanmış",
        )

    lead.assigned_user_id = current_user.id
    lead.status = "aranmadi_ulasma"

    log = LeadLog(
        lead_id=lead.id,
        user_id=current_user.id,
        islem_turu="atandi",
        aciklama=f"{current_user.ad} tarafından üstlenildi",
    )
    db.add(log)
    db.commit()
    db.refresh(lead)
    return _lead_to_out(lead)


@router.get("/my-leads", response_model=list[LeadOut])
def get_my_leads(
    status_filter: str = "",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kullanıcının kendi portföyündeki müşterileri listele."""
    query = db.query(Lead).filter(Lead.assigned_user_id == current_user.id)
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    leads = query.order_by(Lead.eklenme_tarihi.desc()).offset(skip).limit(limit).all()
    return [_lead_to_out(l) for l in leads]


@router.get("/{lead_id}", response_model=LeadDetailOut)
def get_lead_detail(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Müşteri detayı + işlem geçmişi."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    if current_user.rol != "chief" and lead.assigned_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu müşteriye erişim yetkiniz yok")

    logs_out = [
        LeadLogOut(
            id=lg.id,
            islem_turu=lg.islem_turu,
            aciklama=lg.aciklama,
            tarih=lg.tarih,
            user_ad=lg.user.ad if lg.user else None,
        )
        for lg in sorted(lead.logs, key=lambda x: x.tarih or 0, reverse=True)
    ]
    detail = LeadDetailOut(
        id=lead.id,
        isletme_adi=lead.isletme_adi,
        telefon=lead.telefon,
        adres=lead.adres,
        harita_linki=lead.harita_linki,
        eklenme_tarihi=lead.eklenme_tarihi,
        assigned_user_id=lead.assigned_user_id,
        assigned_user_ad=lead.assigned_user.ad if lead.assigned_user else None,
        status=lead.status,
        logs=logs_out,
    )
    return detail


@router.put("/{lead_id}/status", response_model=LeadOut)
def update_status(
    lead_id: int,
    body: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Müşteri aşamasını güncelle."""
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Geçersiz status. Geçerli değerler: {VALID_STATUSES}")

    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    if current_user.rol != "chief" and lead.assigned_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu müşteriye erişim yetkiniz yok")

    old_status = lead.status
    lead.status = body.status

    log = LeadLog(
        lead_id=lead.id,
        user_id=current_user.id,
        islem_turu="durum_degisti",
        aciklama=f"Durum değişti: {old_status} → {body.status}",
    )
    db.add(log)
    db.commit()
    db.refresh(lead)
    return _lead_to_out(lead)


@router.post("/{lead_id}/note", response_model=LeadLogOut)
def add_note(
    lead_id: int,
    body: NoteAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Görüşme notu ekle."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    if current_user.rol != "chief" and lead.assigned_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu müşteriye erişim yetkiniz yok")

    log = LeadLog(
        lead_id=lead.id,
        user_id=current_user.id,
        islem_turu="not_eklendi",
        aciklama=body.aciklama,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return LeadLogOut(
        id=log.id,
        islem_turu=log.islem_turu,
        aciklama=log.aciklama,
        tarih=log.tarih,
        user_ad=current_user.ad,
    )
