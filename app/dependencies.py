from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt
from app.database import SessionLocal
from app.config import settings
from app.models.user import User

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            cred.credentials,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        user = db.query(User).get(payload["sub"])
        if not user:
            raise
        return user
    except:
        raise HTTPException(401, "Invalid token")
