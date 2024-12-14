import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses
from fetcher import URLFetcher


@pytest.mark.asyncio
async def test_fetch_success():
    fetcher = URLFetcher(concurrency=1)
    url = "https://example.com"

    with aioresponses() as m:
        m.get(url, status=200, body="Success")

        async with ClientSession() as session:
            result = await fetcher.fetch(session, url)
            assert result == "Success"


@pytest.mark.asyncio
async def test_fetch_error():
    fetcher = URLFetcher(concurrency=1)
    url = "https://example.com/404"

    with aioresponses() as m:
        m.get(url, status=404)

        async with ClientSession() as session:
            result = await fetcher.fetch(session, url)
            assert "Ошибка при обработке URL" in result


@pytest.mark.asyncio
async def test_fetch_all():
    fetcher = URLFetcher(concurrency=2)
    urls = ["https://example.com/1", "https://example.com/2"]

    with aioresponses() as m:
        m.get("https://example.com/1", status=200, body="Page 1")
        m.get("https://example.com/2", status=404)

        async def get_results():
            results = []
            async for result in fetcher.fetch_all(urls):
                results.append(result)
            return results

        results = await get_results()

        assert len(results) == 2
        assert "Page 1" in results[0]
        assert "Ошибка при обработке URL" in results[1]


@pytest.mark.asyncio
async def test_fetch_all_large_file(tmp_path):
    fetcher = URLFetcher(concurrency=3)
    urls = [f"https://example.com/{i}" for i in range(10)]
    file_path = tmp_path / "urls.txt"
    file_path.write_text("\n".join(urls))

    with aioresponses() as m:
        for url in urls:
            m.get(url, status=200, body=f"Response for {url}")

        async def get_results():
            results = []
            async for result in fetcher.fetch_all(file_path):
                results.append(result)
            return results

        results = await get_results()

        assert len(results) == len(urls)
        for i, result in enumerate(results):
            assert f"Response for https://example.com/{i}" in result
