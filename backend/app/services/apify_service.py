from typing import List
from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.lead_log import LeadLog
from app.schemas.lead import ApifyLeadItem


def import_apify_leads(items: List[ApifyLeadItem], db: Session) -> dict:
    """
    Apify'dan gelen veriyi veritabanına aktar.
    - Telefon bazlı duplicate kontrolü yapar
    - Yeni kayıtlar havuza (assigned_user_id=None) düşer
    """
    eklenen = 0
    atlanan = 0

    for item in items:
        isletme_adi = item.title or "İsimsiz İşletme"
        telefon = _temizle_telefon(item.phone)

        # Duplicate kontrolü: telefon varsa telefona göre, yoksa isme göre
        if telefon:
            mevcut = db.query(Lead).filter(Lead.telefon == telefon).first()
        else:
            mevcut = db.query(Lead).filter(Lead.isletme_adi == isletme_adi).first()

        if mevcut:
            atlanan += 1
            continue

        lead = Lead(
            isletme_adi=isletme_adi,
            telefon=telefon,
            adres=item.address,
            harita_linki=item.url,
            assigned_user_id=None,
            status="havuzda",
        )
        db.add(lead)
        db.flush()  # id'yi al

        log = LeadLog(
            lead_id=lead.id,
            user_id=1,  # sistem kullanıcısı (id=1 chief olmalı)
            islem_turu="apify_import",
            aciklama=f"Apify'dan otomatik import edildi",
        )
        db.add(log)
        eklenen += 1

    db.commit()
    return {"eklenen": eklenen, "atlanan_duplicate": atlanan}


def _temizle_telefon(phone: str | None) -> str | None:
    """Telefon numarasından boşluk ve özel karakterleri temizle."""
    if not phone:
        return None
    temiz = "".join(c for c in phone if c.isdigit() or c == "+")
    return temiz if temiz else None
