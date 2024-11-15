import pytest
import aiohttp
from aiohttp import ClientSession
from fetcher import URLFetcher


@pytest.mark.asyncio
async def test_fetch_success():
    fetcher = URLFetcher(concurrency=1)
    url = "https://httpbin.org/get"
    async with ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        result = await fetcher.fetch(session, url)
        assert "url" in result


@pytest.mark.asyncio
async def test_fetch_error():
    fetcher = URLFetcher(concurrency=1)
    url = "https://httpbin.org/status/404"
    async with ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        result = await fetcher.fetch(session, url)
        assert "Ошибка при обработке URL" in result


@pytest.mark.asyncio
async def test_fetch_all():
    fetcher = URLFetcher(concurrency=2)
    urls = ["https://httpbin.org/get", "https://httpbin.org/status/404"]
    results = await fetcher.fetch_all(urls)
    assert len(results) == 2
    assert "url" in results[0]
    assert "Ошибка при обработке URL" in results[1]
