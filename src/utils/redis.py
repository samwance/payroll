import redis
from typing import Optional
from config.config import redis_settings

REDIS_URL = (
    f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}/0"
)


class RedisClient:
    def __init__(self) -> None:
        self.redis = redis.Redis.from_url(REDIS_URL)

    def set_refresh_token(
        self, user_id: str, refresh_token: str, expires_in: int
    ) -> None:
        self.redis.set(user_id, refresh_token, ex=expires_in)

    def get_refresh_token(self, user_id: str) -> Optional[str]:
        return self.redis.get(user_id)

    def delete_refresh_token(self, user_id: str) -> None:
        self.redis.delete(user_id)

    def is_refresh_token_valid(self, user_id: str, token: str) -> bool:
        stored_token = self.get_refresh_token(user_id)
        return stored_token == token.get(user_id)


redis_client = RedisClient()
