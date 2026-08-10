import re
import logging
from typing import Any
from bs4 import BeautifulSoup
from tqdm import tqdm
from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class WikiScraper(BaseScraper):
    """Parses the population table from a Wikipedia revision

    Cleans the raw HTML and converts the table data into population records.
    """

    def __init__(self):
        super().__init__(url="https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959")
    
    async def parse(self, html: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", {"class": "wikitable"})
        
        if not table:
            logger.error("Could not find 'wikitable' on the page.")
            raise ValueError("Target table not found in HTML.")
        
        results = []
        rows = table.find_all("tr")
        citation_pattern = re.compile(r"\[.*?\]")
        
        for row in tqdm(rows[1:], desc="Parsing Wikipedia table"):
            cols = row.find_all(['th', 'td'])
            
            if len(cols) < 6:
                continue
            
            row_texts = []
            for c in cols:
                text = c.get_text(" ", strip=True)
                text = citation_pattern.sub("", text)
                text = re.sub(r"\s+", " ", text).strip()
                row_texts.append(text)
            
            country = row_texts[0]
            if country == "World" or not country:
                continue
            
            raw_population = row_texts[2]  
            region = row_texts[4]         
            
            clean_pop_str = raw_population.replace(",", "").replace(" ", "").replace("\xa0", "")
            
            try:
                population = int(clean_pop_str)
            except ValueError:
                logger.warning(
                    "Skipping country '%s': invalid population format '%s' (Row data: %s)", 
                    country, clean_pop_str, row_texts
                )
                continue
            
            results.append({
                "country_name": country,
                "region_name": region,
                "population": population,
                "source": "wiki" 
            })
            
        return results