from redis.asyncio import Redis
from core.config import settings

redis = Redis.from_url(str(settings.redis.url), decode_responses=True)
