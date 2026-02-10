from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

class UpdateProfileRequest(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
