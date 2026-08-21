import asyncio
from app.redis import r

cache_ttl = 5 * 60


def cache_url(url: str, metadata: dict):
    r.set(url, metadata, ex=cache_ttl)


async def get_cached_url(url: str):
    key_name = f"url:metadata:{url}"
    value = r.hgetall(key_name)
    return value if value else None


async def get_job_status(job_id: str):
    key_name = f"job:{job_id}"
    status = r.hget(key_name, "status")
    return status
