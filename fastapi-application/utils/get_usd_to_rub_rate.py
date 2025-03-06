import aiohttp

from utils import redis

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
CACHE_KEY = "usd_to_rub_rate"
CACHE_TTL = 3600


async def get_usd_to_rub_rate() -> float:
    cached_rate = await redis.get(CACHE_KEY)
    if cached_rate:
        return float(cached_rate)

    async with aiohttp.ClientSession() as session:
        async with session.get(CBR_URL) as response:
            data = await response.json()
            rate = data["Valute"]["USD"]["Value"]
            await redis.setex(CACHE_KEY, CACHE_TTL, rate)
            return rate
