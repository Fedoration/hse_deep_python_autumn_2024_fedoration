from typing import Union
import argparse
from pathlib import Path
import asyncio
from aiohttp import ClientError
import aiohttp
import aiofiles


class URLFetcher:
    def __init__(self, concurrency: int):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        """Асинхронно загружает контент URL."""
        try:
            async with self.semaphore:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
        except ClientError as e:
            return f"Ошибка при обработке URL {url}: {e}"

    async def fetch_all(self, urls: Union[Path, list[str]]):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            tasks = []
            if isinstance(urls, Path):
                async with aiofiles.open(urls, mode="r") as file:
                    async for line in file:
                        url = line.strip()
                        if url:
                            tasks.append(self.fetch(session, url))
                            if len(tasks) >= self.concurrency:
                                for result in await asyncio.gather(*tasks):
                                    yield result
                                tasks = []
            elif isinstance(urls, list):
                for url in urls:
                    tasks.append(self.fetch(session, url))
                    if len(tasks) >= self.concurrency:
                        for result in await asyncio.gather(*tasks):
                            yield result
                        tasks = []
            if tasks:
                for result in await asyncio.gather(*tasks):
                    yield result


async def main(concurrency: int, urls_file: Path):
    """Основная функция для обработки URL-ов."""
    fetcher = URLFetcher(concurrency)
    async for result in fetcher.fetch_all(urls_file):
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(result + "\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронная обкачка URL-ов.")
    parser.add_argument(
        "concurrency", type=int, help="Количество одновременных запросов."
    )
    parser.add_argument("urls_file", type=Path, help="Файл со списком URL-ов.")
    args = parser.parse_args()

    asyncio.run(main(args.concurrency, args.urls_file))
