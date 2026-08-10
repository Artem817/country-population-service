from scrapers.base import BaseScraper
from scrapers.wiki import WikiScraper
from scrapers.stats_times import StatsTimesScraper 

class ScraperFactory:
    """Factory class to instantiate the appropriate scraper based on source name."""
    
    @staticmethod
    def get_scraper(source_name: str) -> BaseScraper:
        """Returns an instance of a BaseScraper subclass.

        Args:
            source_name: The identifier of the data source 'wiki' and 'stats' 

        Returns:
            An instantiated scraper object.

        Raises:
            ValueError: If the source_name is not supported.
        """
        source_name = source_name.lower().strip()
        
        if source_name == "wiki":
            return WikiScraper()
        elif source_name == "stats":
            return StatsTimesScraper()
        else:
            raise ValueError(f"Unknown data source requested: {source_name}")
        
