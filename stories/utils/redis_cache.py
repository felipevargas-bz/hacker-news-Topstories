import redis
from django.conf import settings
from typing import Any, List, Dict
import json


def get_redis_cache(i: int, n: int):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    items: List[int] = []
    for key in redis_instance.keys("*"):
        if key.decode('utf-8') != 'ids':
            items.append(json.loads(redis_instance.get(key)))
    try:
        stories = items[int(i):int(n)]
    except Exception:
        stories = []
    return stories

def save_redis_cache(items: List[Dict[str, Any]]):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    for item in items:
        redis_instance.set(item['ID'], json.dumps(item), ex=10)


def save_ids_redis_cache(ids: List[int]):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    redis_instance.set('ids', json.dumps(ids), ex=10)


def ids_redis_cache():
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    ids = redis_instance.get('ids')
    if ids:
        ids = json.loads(ids)
    else:
        ids = []
    return ids
