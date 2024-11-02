from datetime import timedelta
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer
from config.config import jwt_settings

access_security = JwtAccessBearerCookie(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(
        minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRES
    ),
)

refresh_security = JwtRefreshBearer(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(
        minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
    ),
)
