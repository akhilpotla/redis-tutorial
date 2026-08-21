import json
import redis

from worker.worker import get_url_metadata

cache_ttl = 5 * 60
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

try:
    r.ping()
    while True:
        _, job = r.brpop("jobs")
        job_dict = json.loads(job)
        url = job_dict["url"]
        job_id = job_dict["job_id"]
        url_key_name = f"url:metadata:{url}"
        job_id_key_name = f"job:{job_id}"
        r.hset(job_id_key_name, "status", "processing")
        status_code, title = get_url_metadata(url)
        status = "failed" if status_code >= 400 else "complete"
        r.hset(url_key_name, "title", title)
        r.hset(url_key_name, "status_code", status_code)
        r.hset(job_id_key_name, "status", status)
        r.set(
            url, json.dumps({"title": title, "status_code": status_code}), ex=cache_ttl
        )
except Exception as e:
    print(f"Error: {e}")
