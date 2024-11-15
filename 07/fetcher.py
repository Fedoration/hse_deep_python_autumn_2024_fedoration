import argparse
from pathlib import Path
import asyncio
from aiohttp import ClientError
import aiohttp


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

    async def fetch_all(self, urls: list[str]) -> list[str]:
        """Асинхронно обрабатывает список URL-ов."""
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            tasks = [self.fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)


async def main(concurrency: int, urls_file: Path):
    """Основная функция для обработки URL-ов."""
    urls = urls_file.read_text().splitlines()
    fetcher = URLFetcher(concurrency)
    results = await fetcher.fetch_all(urls)

    # Сохраняем результаты в файл
    with open("results.txt", "w", encoding="utf-8") as f:
        for url, content in zip(urls, results):
            f.write(f"{url}:\n{content}\n{'-' * 80}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронная обкачка URL-ов.")
    parser.add_argument(
        "concurrency", type=int, help="Количество одновременных запросов."
    )
    parser.add_argument("urls_file", type=Path, help="Файл со списком URL-ов.")
    args = parser.parse_args()

    asyncio.run(main(args.concurrency, args.urls_file))
