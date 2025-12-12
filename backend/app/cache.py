import os
import redis.asyncio as redis
import json
from datetime import datetime
from typing import Optional, Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class CacheService:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        self.stats_key = "cache:analytics"

    async def get(self, key: str) -> Optional[Any]:
        val = await self.redis.get(key)
        timestamp = datetime.utcnow().isoformat()
        if val:
            await self.redis.hincrby(self.stats_key, "hits", 1)
            # Log Event
            await self.redis.lpush("cache:logs", json.dumps({"key": key, "type": "HIT", "time": timestamp}))
            await self.redis.ltrim("cache:logs", 0, 49) # Keep execution 50 logs
            try:
                return json.loads(val)
            except:
                return val
        else:
            await self.redis.hincrby(self.stats_key, "misses", 1)
             # Log Event
            await self.redis.lpush("cache:logs", json.dumps({"key": key, "type": "MISS", "time": timestamp}))
            await self.redis.ltrim("cache:logs", 0, 49)
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await self.redis.set(key, value, ex=ttl)

    async def get_stats(self) -> dict:
        stats = await self.redis.hgetall(self.stats_key)
        logs = await self.redis.lrange("cache:logs", 0, -1)
        parsed_logs = [json.loads(l) for l in logs]
        
        hits = int(stats.get("hits", 0))
        misses = int(stats.get("misses", 0))
        total = hits + misses
        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hits / total, 2) if total > 0 else 0,
            "logs": parsed_logs
        }
    
    async def clear_stats(self):
        await self.redis.delete(self.stats_key)
        await self.redis.delete("cache:logs")

    async def block_token(self, token: str, ttl: int = 3600):
        """Block a JWT token until its expiration."""
        key = f"blocklist:{token}"
        await self.redis.set(key, "blocked", ex=ttl)

    async def is_token_blocked(self, token: str) -> bool:
        """Check if a token is in the blocklist."""
        key = f"blocklist:{token}"
        return await self.redis.exists(key) > 0

# Global Instance
cache = CacheService()
