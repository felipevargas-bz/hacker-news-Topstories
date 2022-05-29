import asyncio
from typing import Any, List, Dict
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        storie = await response.json()
        return {
            'titulo': storie['title'],
            'ID': storie['id']
        }


async def run_requests(storie_ids: List[int]) -> List[Dict[str, Any]]:
    urls = ['https://hacker-news.firebaseio.com/v0/item/'\
        + str(storie_id) + '.json?print=pretty' for storie_id in storie_ids]

    stories: List[Dict[str, Any]] = []

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        stories = await asyncio.gather(*tasks)

    return stories
