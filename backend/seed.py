import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    try:
        # Chief kullanıcısı var mı kontrol et
        chief = db.query(User).filter(User.email == "admin@catering.com").first()
        if not chief:
            chief = User(
                ad="Ahmet Yönetici",
                email="admin@catering.com",
                password_hash=get_password_hash("admin123"),
                rol="chief"
            )
            db.add(chief)
            db.commit()
            print("✅ Chief kullanıcısı oluşturuldu: admin@catering.com / admin123")
        else:
            print("ℹ️ Chief kullanıcısı zaten mevcut")
        
        # Örnek pazarlamacı
        marketing = db.query(User).filter(User.email == "pazarlama@catering.com").first()
        if not marketing:
            marketing = User(
                ad="Ayşe Pazarlama",
                email="pazarlama@catering.com",
                password_hash=get_password_hash("pazarlama123"),
                rol="marketing"
            )
            db.add(marketing)
            db.commit()
            print("✅ Pazarlamacı oluşturuldu: pazarlama@catering.com / pazarlama123")
        else:
            print("ℹ️ Pazarlamacı zaten mevcut")
            
    finally:
        db.close()

if __name__ == "__main__":
    seed()
