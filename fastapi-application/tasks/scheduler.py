from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tasks.calculate_delivery_cost import calculate_delivery_cost

scheduler = AsyncIOScheduler()
scheduler.add_job(calculate_delivery_cost, "interval", minutes=5)
