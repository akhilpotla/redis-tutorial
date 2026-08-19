import json
import redis

from worker.worker import get_url_metadata

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

try:
    r.ping()
    while True:
        _, job = r.brpop("jobs")
        job_dict = json.loads(job)
        url = job_dict["url"]
        status_code, title = get_url_metadata(url)
        key_name = f"url:metadata:{url}"
        r.hset(key_name, "title", title)
        r.hset(key_name, "status_code", status_code)
except Exception as e:
    print(f"Error: {e}")
