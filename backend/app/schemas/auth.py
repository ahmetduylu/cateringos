from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    ad: str
    rol: str


class UserMe(BaseModel):
    id: int
    ad: str
    email: str
    rol: str

    class Config:
        from_attributes = True
