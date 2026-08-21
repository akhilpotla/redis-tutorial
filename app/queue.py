import json
import uuid
from datetime import datetime

from app.redis import r

queue_name = "jobs"


async def enqueue_url(url: str):
    job_id = uuid.uuid5(uuid.NAMESPACE_URL, url)
    json_string = json.dumps({"url": url, "job_id": str(job_id)})
    r.lpush(queue_name, json_string)
    key_name = f"job:{job_id}"
    created_at = datetime.now().timestamp()
    r.hset(key_name, "status", "queued")
    r.hset(key_name, "url", url)
    r.hset(key_name, "created_at", created_at)
    return job_id


async def dequeue_url():
    result = r.brpop(queue_name, timeout=0)
    return result
