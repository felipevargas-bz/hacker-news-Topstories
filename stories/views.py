from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
import requests as req
import json
from rest_framework.decorators import api_view
import asyncio
from stories.utils.run_requests import run_requests
from stories.utils.redis_cache import get_redis_cache, save_redis_cache, ids_redis_cache, save_ids_redis_cache
from typing import List, Dict, Any

# Create your views here.

@api_view(['GET'])
def stories(request):
    try:
        url_stories_id = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        i = request.GET.get('i') if request.GET.get('i') else 0
        n = request.GET.get('n') if request.GET.get('n') else -1
        stories: List[Dict[str, Any]] = []

        stories = get_redis_cache(i=int(i), n=int(n))

        if not stories:
            response = ids_redis_cache()

            if not response:
                response = req.get(url_stories_id).json()
                save_ids_redis_cache(response)
            storie_ids = response[int(i):int(n)]
            storie_ids.sort()

            stories  = asyncio.run(run_requests(storie_ids))

            save_redis_cache(items=stories)

        return JsonResponse(stories, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False)
