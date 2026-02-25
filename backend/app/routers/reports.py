from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_current_user, require_chief
from app.database import get_db
from app.models.lead import Lead
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/team")
def team_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chief),
):
    """
    Personel bazlı rapor:
    Her pazarlamacı için toplam, kazanılan ve aktif müşteri sayısı.
    """
    marketing_users = db.query(User).filter(User.rol == "marketing").all()
    result = []
    for user in marketing_users:
        total = db.query(func.count(Lead.id)).filter(Lead.assigned_user_id == user.id).scalar()
        kazanilan = (
            db.query(func.count(Lead.id))
            .filter(Lead.assigned_user_id == user.id, Lead.status == "kazanildi")
            .scalar()
        )
        ilgilenmiyor = (
            db.query(func.count(Lead.id))
            .filter(Lead.assigned_user_id == user.id, Lead.status == "ilgilenmiyor")
            .scalar()
        )
        aktif = total - kazanilan - ilgilenmiyor
        donusum_orani = round((kazanilan / total * 100), 1) if total > 0 else 0.0

        result.append(
            {
                "user_id": user.id,
                "ad": user.ad,
                "email": user.email,
                "toplam_musteri": total,
                "kazanilan": kazanilan,
                "ilgilenmiyor": ilgilenmiyor,
                "aktif": aktif,
                "donusum_orani": donusum_orani,
            }
        )
    return result


@router.get("/pool-stats")
def pool_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chief),
):
    """Havuz ve genel istatistikler."""
    toplam = db.query(func.count(Lead.id)).scalar()
    havuzda = db.query(func.count(Lead.id)).filter(Lead.assigned_user_id.is_(None)).scalar()
    atanmis = toplam - havuzda
    kazanilan = db.query(func.count(Lead.id)).filter(Lead.status == "kazanildi").scalar()
    ilgilenmiyor = db.query(func.count(Lead.id)).filter(Lead.status == "ilgilenmiyor").scalar()
    aktif = atanmis - kazanilan - ilgilenmiyor

    # Status bazlı dağılım
    status_dist = (
        db.query(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
        .all()
    )

    return {
        "toplam_musteri": toplam,
        "havuzda": havuzda,
        "atanmis": atanmis,
        "kazanilan": kazanilan,
        "ilgilenmiyor": ilgilenmiyor,
        "aktif": aktif,
        "status_dagilimi": {s: c for s, c in status_dist},
    }


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chief),
):
    """Şef ana dashboard verileri."""
    toplam = db.query(func.count(Lead.id)).scalar()
    havuzda = db.query(func.count(Lead.id)).filter(Lead.assigned_user_id.is_(None)).scalar()
    kazanilan = db.query(func.count(Lead.id)).filter(Lead.status == "kazanildi").scalar()
    personel_sayisi = db.query(func.count(User.id)).filter(User.rol == "marketing").scalar()

    return {
        "toplam_musteri": toplam,
        "havuzda": havuzda,
        "kazanilan": kazanilan,
        "personel_sayisi": personel_sayisi,
    }
