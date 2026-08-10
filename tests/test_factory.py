from scrapers.factory import ScraperFactory
from scrapers.stats_times import StatsTimesScraper
from scrapers.wiki import WikiScraper

def test_get_wiki_scraper():
    scraper = ScraperFactory.get_scraper("wiki")
    assert isinstance(scraper, WikiScraper)
    assert scraper.url == "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"

def test_get_stats_scraper():
    scraper = ScraperFactory.get_scraper("stats")
    assert isinstance(scraper, StatsTimesScraper)