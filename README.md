# hacker-news-Topstories

This application is based on consulting the topstories in hackernews through its API, the first thing we do is consult the topstories which only brings us the id of the latest news, then we consult again but this time to obtain the details of the news, the idea The main one is to show the details of the n news that the user wants, that is, if our API is sent i=0 and n=30, it must show the first 30 news of the entire list of news.
Finally, a cache was made in redis, to save the news that has been consulted before, and save them for 10s.

## Important libraries
* [redis 4.3.1](https://pypi.org/project/redis/)
Used to create the connection to the redis database engine.
* [aiohttp 3.8.1](https://pypi.org/project/pdf2image/)
Used to asynchronously make requests to the Hacker News API.


## Technologies
* [Python](https://www.python.org/)
* [redis](https://redis.io/)
* [Docker](https://www.docker.com/)
* [Django](https://www.djangoproject.com/)


## Installation

### Requirements
* docker
* docker-compose
* git

```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

## Usage

To query the news, you must first run the project or use the version deployed in aws, which is at the following [URL](http://pdf-extraction.felipevargas.tech:8088/stories/?i=5&n=30).


