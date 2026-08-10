import asyncio
import logging
import sys
import os
from db import DatabaseManager
from scrapers.factory import ScraperFactory
import logger as custom_logger

async def main() -> None:
    custom_logger.setup_logging()
    logger = logging.getLogger(__name__)
    
    
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")  
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "population_db")
    
    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    db_manager = DatabaseManager(db_url) 
    data_source = os.getenv("DATA_SOURCE", "wiki")
    scraper = ScraperFactory.get_scraper(data_source)
    try:
        logger.info("Starting data ingestion pipeline..")
        
        await db_manager.init_db()
        countries_data = await scraper.run()
        await db_manager.save_countries(countries_data)
        
        logger.info("Pipeline executed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    asyncio.run(main())