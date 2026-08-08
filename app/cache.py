from app.redis import r

cache_ttl = 5 * 60


def cache_url(url: str, metadata: dict):
    r.set(url, metadata, ex=cache_ttl)


def get_cached_url(url: str):
    value = r.get(url)
    return eval(value) if value else None
