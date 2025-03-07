import logging
from decimal import Decimal

import aiohttp

from .redis_init import redis

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
CACHE_KEY = "usd_to_rub_rate"
CACHE_TTL = 3600

log = logging.getLogger(__name__)


async def get_usd_to_rub_rate() -> Decimal:
    cached_rate = await redis.get(CACHE_KEY)
    if cached_rate:
        rate = Decimal(cached_rate)

    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(CBR_URL) as response:
                    data = await response.json(content_type=None)
                    rate = data["Valute"]["USD"]["Value"]
                    await redis.setex(CACHE_KEY, CACHE_TTL, rate)
                    rate = Decimal(rate)

        except Exception as e:
            log.error(f"Ошибка получения курса: {str(e)}", exc_info=True)
            raise Exception(f"Не удалось получить курс USD/RUB: {str(e)}")

    return rate
