from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.lead import ApifyLeadItem
from app.services.apify_service import import_apify_leads

router = APIRouter(prefix="/apify", tags=["apify"])


@router.post("/webhook")
def apify_webhook(
    items: List[ApifyLeadItem],
    db: Session = Depends(get_db),
):
    """
    Apify'dan gelen Google Maps verilerini havuza ekler.
    Apify aktörü bittiğinde bu endpoint'i 'Run Finished' webhook olarak çağırır.
    Telefon bazlı deduplication uygulanır — aynı telefon tekrar eklenmez.
    """
    if not items:
        return {"mesaj": "Gelen veri boş", "eklenen": 0, "atlanan_duplikat": 0}

    result = import_apify_leads(items, db)
    return {
        "mesaj": f"{result['eklenen']} yeni kayıt eklendi, {result['atlanan_duplicate']} duplikat atlandı",
        "eklenen": result["eklenen"],
        "atlanan_duplikat": result["atlanan_duplicate"],
    }
