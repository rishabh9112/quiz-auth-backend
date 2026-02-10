import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    token = Column(String, nullable=False)
    expiry_time = Column(DateTime, nullable=False)
