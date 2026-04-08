import json
import redis.asyncio as redis  # type: ignore
from typing import Optional, Dict, Any
from ..core.config import settings
import structlog

logger = structlog.get_logger()

class CacheService:
    def __init__(self):
        self.redis = None
        if settings.REDIS_URL:
            try:
                self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
                logger.info("redis_connected", url=settings.REDIS_URL)
            except Exception as e:
                logger.error("redis_connection_failed", error=str(e))
        else:
            logger.info("redis_disabled", reason="REDIS_URL not set")

    async def get_analysis(self, username: str) -> Optional[Dict[str, Any]]:
        if not self.redis:
            return None
            
        try:
            cached_data = await self.redis.get(f"analysis:{username.lower()}")
            if cached_data:
                logger.info("cache_hit", username=username)
                return json.loads(cached_data)
        except Exception as e:
            logger.warning("cache_read_error", error=str(e))
            
        return None

    async def set_analysis(self, username: str, data: Dict[str, Any], expire_seconds: int = 86400):
        if not self.redis:
            return
            
        try:
            await self.redis.set(
                f"analysis:{username.lower()}", 
                json.dumps(data),
                ex=expire_seconds
            )
            logger.info("cache_set", username=username, expire_seconds=expire_seconds)
        except Exception as e:
            logger.warning("cache_write_error", error=str(e))
            
    async def rate_limit(self, ip: str, limit: int = 10, window: int = 60) -> bool:
        if not self.redis:
            return True # If Redis is offline, allow.
            
        key = f"rate_limit:{ip}"
        try:
            current = await self.redis.get(key)
            if current and int(current) >= limit:
                return False
                
            pipe = self.redis.pipeline()
            pipe.incr(key)
            if not current:
                pipe.expire(key, window)
            await pipe.execute()
            return True
        except Exception as e:
            logger.warning("rate_limit_error", error=str(e))
            return True

    async def close(self):
        if self.redis:
            await self.redis.close()

cache_service = CacheService()
