from app.redis import r


def cache_url(url: str, metadata: dict):
    r.set(url, metadata, ex=60)


def get_cached_url(url: str):
    value = r.get(url)
    return eval(value) if value else None
