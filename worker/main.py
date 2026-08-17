import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

try:
    r.ping()
    while True:
        _, job = r.brpop("jobs")
        print(f"Job: {job}")
except Exception as e:
    print(f"Error: {e}")
