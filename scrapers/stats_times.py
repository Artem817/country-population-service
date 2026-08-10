import logging
from typing import Any
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class StatsTimesScraper(BaseScraper):
    """Parses the population table from StatisticsTimes.com"""
    
    def __init__(self):
        super().__init__(url="https://statisticstimes.com/demographics/countries-by-population.php")
        
    async def parse(self, html: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", {"id": "table_id"})
        if not table:
            logger.error("Could not find table with id='table_id' on StatisticsTimes.")
            raise ValueError("Target table not found in HTML.")

        results = []
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

        for row in rows:
            name_cells = row.find_all("td", class_="name")
            data_cells = row.find_all("td", class_="data")

            if not name_cells or not data_cells:
                continue

            country = name_cells[0].get_text(" ", strip=True)
            region = name_cells[1].get_text(" ", strip=True) if len(name_cells) > 1 else None
            raw_population = data_cells[0].get_text(strip=True)

            if not country or country.lower() == "world":
                continue

            if not region:
                logger.warning(f"Skipping '{country}': missing region")
                continue

            clean_pop_str = raw_population.replace(",", "").replace(" ", "")

            try:
                population = int(clean_pop_str)
            except ValueError:
                logger.warning(f"Skipping '{country}': invalid pop format '{clean_pop_str}'")
                continue

            results.append({
                "country_name": country,
                "region_name": region,
                "population": population,
                "source": "stats",
            })

        return results
