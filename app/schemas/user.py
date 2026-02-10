from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
