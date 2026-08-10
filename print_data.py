import asyncio
import os
import sys
import logging

from db import DatabaseManager
import logger as custom_logger

async def main() -> None:
    custom_logger.setup_logging("ERROR")
    logger = logging.getLogger(__name__)

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost") 
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "population_db")

    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db_manager = DatabaseManager(db_url)

    try:
        await db_manager.init_db()
        data = await db_manager.get_aggregated_data()
        
        if not data:
            print("Database's empty. First, run get_data.")
            return

        for row in data:
            print(row["region_name"])
            print(row["total_population"])
            print(row["max_country"])
            print(row["max_pop"])
            print(row["min_country"])
            print(row["min_pop"])
            
    except Exception as e:
        logger.error(f"Failed to print data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())