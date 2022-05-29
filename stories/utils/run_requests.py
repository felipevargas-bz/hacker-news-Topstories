import asyncio
from typing import Any, List, Dict
import aiohttp


async def fetch(session, url):
    """Fetch a given URL

    Args:
        session (_type_): The session object.
        url (_type_): The url to fetch.

    Returns:
        Dict[str, Any]: The news.
    """
    async with session.get(url) as response:
        storie = await response.json()
        return {
            'titulo': storie['title'],
            'ID': storie['id']
        }


async def run_requests(storie_ids: List[int]) -> List[Dict[str, Any]]:
    """Run the requests in parallel.

    Args:
        storie_ids (List[int]): The list of ids.

    Returns:
        List[Dict[str, Any]]: The list of news.
    """
    urls = ['https://hacker-news.firebaseio.com/v0/item/'\
        + str(storie_id) + '.json?print=pretty' for storie_id in storie_ids]

    stories: List[Dict[str, Any]] = []

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        stories = await asyncio.gather(*tasks)

    return stories
