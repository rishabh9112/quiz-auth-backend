from datetime import timedelta
from app.utils.jwt import create_token
from app.config import settings

def generate_tokens(user_id: str):
    access = create_token(
        {"sub": user_id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh = create_token(
        {"sub": user_id},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return access, refresh
