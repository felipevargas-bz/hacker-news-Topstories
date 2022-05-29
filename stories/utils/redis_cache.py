import redis
from django.conf import settings
from typing import Any, List, Dict
import json


def get_redis_cache(i: int, n: int) -> List[Dict[str, Any]]:
    """Query and return the details of the [n] amount of news that the user

    Args:
        i (int): The index of the news to start.
        n (int): The amount of news to return.

    Returns:
        List[Dict[str, Any]] : The list of news.
    """
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


def save_redis_cache(items: List[Dict[str, Any]]) -> None:
    """Save the news in redis.

    Args:
        items (List[Dict[str, Any]]): The list of news.
    """
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    for item in items:
        redis_instance.set(item['ID'], json.dumps(item), ex=10)


def save_ids_redis_cache(ids: List[int]) -> None:
    """Save the ids in redis.

    Args:
        ids (List[int]): The list of ids.
    """
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    redis_instance.set('ids', json.dumps(ids), ex=10)


def ids_redis_cache() -> List[int]:
    """Query and return the ids of the news.

    Returns:
        List[int]: The list of ids.
    """
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    ids = redis_instance.get('ids')
    if ids:
        ids = json.loads(ids)
    else:
        ids = []
    return ids
