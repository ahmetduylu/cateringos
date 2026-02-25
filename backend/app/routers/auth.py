from datetime import timedelta
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import verify_password, create_access_token, get_password_hash
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserMe
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
        
        # Debug password
        print(f"Input password length: {len(request.password)}")
        print(f"Stored hash: {user.password_hash[:50]}...")
        
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
        
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return TokenResponse(
            access_token=access_token,
            user_id=user.id,
            ad=user.ad,
            rol=user.rol,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserMe)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/setup")
def setup_users(db: Session = Depends(get_db)):
    """İlk kullanıcıları oluştur"""
    try:
        # Mevcut kullanıcıları kontrol et
        existing = db.query(User).filter(User.email == "admin@catering.com").first()
        if existing:
            return {"message": "Kullanıcılar zaten mevcut"}
        
        # Chief kullanıcısı
        admin = User(
            ad="Ahmet Yönetici",
            email="admin@catering.com",
            password_hash=get_password_hash("admin123"),
            rol="chief"
        )
        db.add(admin)
        
        # Marketing kullanıcısı
        marketing = User(
            ad="Ayşe Pazarlama",
            email="pazarlama@catering.com",
            password_hash=get_password_hash("pazarlama123"),
            rol="marketing"
        )
        db.add(marketing)
        
        db.commit()
        return {"message": "Kullanıcılar oluşturuldu"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    user = User(
        ad=body.ad,
        email=body.email,
        password_hash=get_password_hash(body.password),
        rol=body.rol,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
