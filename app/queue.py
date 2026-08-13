import uuid

from app.redis import r

queue_name = "jobs"


async def enqueue_url(url: str):
    job_id = uuid.UUID(url)
    r.lpush(queue_name, {"url": url, "job_id": job_id})
    return job_id


async def dequeue_url():
    result = r.brpop(queue_name, timeout=0)
    return result
