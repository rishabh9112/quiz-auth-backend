import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.utils.hashing import hash_password, verify_password
from app.utils.password_validator import validate_password
from app.services.token_service import generate_tokens
from app.services.email_service import send_reset_email

def register_user(db: Session, full_name, email, password):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")

    validate_password(password)

    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access, refresh = generate_tokens(user.id)
    return access, refresh, user

def login_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    return (*generate_tokens(user.id), user)

def create_reset_token(db: Session, email):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return

    token = str(uuid.uuid4())

    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expiry_time=datetime.utcnow() + timedelta(hours=1),
    )

    db.add(reset)
    db.commit()
    send_reset_email(email, token)

def reset_password(db: Session, token, password):
    record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()

    if not record or record.expiry_time < datetime.utcnow():
        raise HTTPException(400, "Invalid or expired token")

    validate_password(password)

    user = db.query(User).get(record.user_id)
    user.hashed_password = hash_password(password)

    db.delete(record)
    db.commit()
