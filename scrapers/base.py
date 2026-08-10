from abc import ABC, abstractmethod
from typing import Any
import aiohttp
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self,url:str, headers: dict[str,str] | None = None) -> None:
        self.url = url
        self.headers = headers or {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        self.timeout = aiohttp.ClientTimeout(total=10)
        
    async def fetch_html(self) -> str:
        """Asynchronously receives raw data from an HTML link
        Returns:
            The raw HTML content as a string.

        Raises:
            aiohttp.ClientError: If an HTTP or connection error occurs.
        """
        logger.info("Fetching HTML from: %s", self.url)   
        
        async with aiohttp.ClientSession(headers=self.headers,timeout=self.timeout) as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                html = await response.text()
                logger.info("Successfully downloaded HTML (%d bytes)", len(html))
                return html
            
    @abstractmethod
    async def parse(self,html: str) -> list[dict[str,Any]]:
        """Parse raw HTML into structured population records.
        """
        pass                

    async def run(self) -> list[dict[str, Any]]:
        """Fetch HTML and parse data (orchestrating)."""
        logger.info("Starting scraper pipeline: %s", self.__class__.__name__)
        html = await self.fetch_html()
        data = await self.parse(html)
        logger.info(
            "Successfully extracted %d records using %s",
            len(data),
            self.__class__.__name__,
        )
        return data