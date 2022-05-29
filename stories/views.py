from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
import requests as req
import logging
from rest_framework.decorators import api_view
import asyncio
from stories.utils.run_requests import run_requests
from stories.utils.redis_cache import (get_redis_cache, save_redis_cache,
                                       ids_redis_cache, save_ids_redis_cache)
from typing import List, Dict, Any

log = logging.getLogger(__name__)


@api_view(['GET'])
def stories(request):
    """Query and return the details of the [n] amount of news that the user
       wants to see. storing a cache created in redis to later
       consult said information.

    Args:
        request Any: The request object.

    Returns:
        List[Dict[str, Any]]: The list of news.
    """
    try:
        url_stories_id = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        i = request.GET.get('i') if request.GET.get('i') else 0
        n = request.GET.get('n') if request.GET.get('n') else -1
        stories: List[Dict[str, Any]] = []

        log.info('Requesting stories from redis cache')
        stories = get_redis_cache(i=int(i), n=int(n))

        if not stories:
            log.info('stories not found in redis cache')

            response = ids_redis_cache()

            if not response:
                log.info('ids not found in redis cache')

                log.info('Requesting ids from hacker-news')
                response = req.get(url_stories_id).json()

                log.info('Saving ids in redis cache')
                save_ids_redis_cache(response)
            storie_ids = response[int(i):int(n)]
            storie_ids.sort()

            log.info('Requesting stories from hacker-news')
            stories  = asyncio.run(run_requests(storie_ids))

            log.info('Saving stories in redis cache')
            save_redis_cache(items=stories)

        return JsonResponse(stories, safe=False)

    except Exception as e:
        log.error(e)
        return JsonResponse({'error': str(e)}, safe=False)
