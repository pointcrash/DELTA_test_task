import logging
from decimal import Decimal

import aiohttp

from .redis_init import redis

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
CACHE_KEY = "usd_to_rub_rate"
CACHE_TTL = 3600

log = logging.getLogger(__name__)


async def get_usd_to_rub_rate() -> Decimal:
    """
    Retrieve the current USD to RUB exchange rate from cache or CBR API.
    """
    try:
        cached_rate = await redis.get(CACHE_KEY)
        if cached_rate:
            rate = Decimal(cached_rate)

    except Exception:
        log.error("Connection Redis error", exc_info=True)
        raise Exception("Connection Redis error")

    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(CBR_URL) as response:
                    data = await response.json(content_type=None)
                    rate = data["Valute"]["USD"]["Value"]
                    await redis.setex(CACHE_KEY, CACHE_TTL, rate)
                    rate = Decimal(rate)

        except Exception as e:
            log.error("Error getting rate", exc_info=True)
            raise Exception("Error getting rate")

    return rate
