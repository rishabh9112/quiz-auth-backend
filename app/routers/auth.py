from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.auth import *
from app.schemas.user import UserResponse
from app.services.auth_service import *
from app.utils.hashing import verify_password, hash_password
from app.utils.password_validator import validate_password

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    access, refresh, user = register_user(db, **data.model_dump())

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": UserResponse.model_validate(user),
    }

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    access, refresh, user = login_user(db, data.email, data.password)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": UserResponse.model_validate(user),
    }

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
def forgot(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    create_reset_token(db, data.email)
    return {"message": "If email exists, reset token generated"}

@router.post("/reset-password")
def reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_password(db, data.token, data.password)
    return {"message": "Password reset successful"}

@router.get("/profile", response_model=UserResponse)
def profile(user=Depends(get_current_user)):
    return user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: UpdateProfileRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.full_name:
        user.full_name = data.full_name

    if data.email:
        user.email = data.email

    db.commit()
    db.refresh(user)
    return user

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(400, "Old password incorrect")

    validate_password(data.new_password)
    user.hashed_password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated"}
