import aioredis

import json

try:
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
except:
    redis = None


class CacheManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        @staticmethod
        async def fetch_from_cache(redis_name: str, refresh_ttl: bool = False, ttl: int = 3600):
            if redis is None:
                return None
            try:
                cached_data = await redis.get(redis_name)
                if cached_data:
                    self.logging.debug(f"{redis_name} found in cache.")
                    if refresh_ttl:
                        await redis.expire(redis_name, ttl)  # Rafraîchit le TTL
                        self.logging.debug(f"TTL refreshed for {redis_name}.")
                    try:
                        return json.loads(cached_data)  # Convertir le JSON en objet Python si possible
                    except json.JSONDecodeError:
                        return cached_data  # Retourne tel quel si ce n'est pas du JSON
                return cached_data
            except Exception as e:
                self.logging.warning(f"Redis error while fetching {redis_name}: {str(e)}")
                return None

        @staticmethod
        async def store_in_cache(redis_name: str, redis_content, ttl: int = 3600):
            if redis is None:
                return None
            try:
                if not isinstance(redis_content, str):
                    redis_content = json.dumps(redis_content)
                await redis.setex(redis_name, ttl, redis_content)
                self.logging.debug(f"{redis_name} cached in Redis  with TTL {ttl}.")
                return True
            except Exception as e:
                self.logging.warning(f"Redis error while caching {redis_name}: {str(e)}")
                return False

        @staticmethod
        async def remove_from_cache(redis_name: str):
            if redis is None:
                return False
            try:
                await redis.delete(redis_name)
                self.logging.debug(f"{redis_name} removed from Redis cache.")
                return True
            except Exception as e:
                self.logging.warning(f"Redis error while removing {redis_name} from cache: {str(e)}")
                return False
