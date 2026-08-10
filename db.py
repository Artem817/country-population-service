import logging
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from typing import Any
from models import CountryPopulation, Base
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func, case

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self,db_url: str):
        self.engine = create_async_engine(db_url,echo = False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    async def init_db(self) -> None:
        """Initialize the database scheme"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def save_countries(self,countries_data : list[dict[str,Any]]) -> None:
        if not countries_data:
            logger.warning("No data provided to save")
            return
        
        logger.info(f"Saving {len(countries_data)} records to the database")
        
        async with self.async_session() as session:
            try:
                await session.execute(delete(CountryPopulation))
                db_object = [
                    CountryPopulation(**record) for record in countries_data
                ]
                
                session.add_all(db_object)
                await session.commit()
                logger.info("Successfully saved all records")   
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error("Database error during save_countries: %s", e)
                raise
    
    async def get_aggregated_data(self) -> list[dict]:
        """Fetch aggregated region data using SQLAlchemy ORM expressions."""
        async with self.async_session() as session:
            try:
                max_rank = func.row_number().over(
                    partition_by=CountryPopulation.region_name,
                    order_by=(
                        CountryPopulation.population.desc(),
                        CountryPopulation.country_name.asc(),
                    )
                ).label("max_rank")

                min_rank = func.row_number().over(
                    partition_by=CountryPopulation.region_name,
                    order_by=(
                        CountryPopulation.population.asc(),
                        CountryPopulation.country_name.asc(),
                    )
                ).label("min_rank")
                
                ranked_cte = (
                    select(
                        CountryPopulation.region_name,
                        CountryPopulation.country_name,
                        CountryPopulation.population,
                        max_rank,
                        min_rank,
                    )
                    .cte("ranked_countries")
                    )

                stmt = (
                    select(
                        ranked_cte.c.region_name,
                        func.sum(ranked_cte.c.population).label("total_population"),
                        func.max(
                            case((ranked_cte.c.max_rank == 1, ranked_cte.c.country_name))
                        ).label("max_country"),
                        func.max(
                            case((ranked_cte.c.max_rank == 1, ranked_cte.c.population))
                        ).label("max_pop"),
                        func.max(
                            case((ranked_cte.c.min_rank == 1, ranked_cte.c.country_name))
                        ).label("min_country"),
                        func.max(
                            case((ranked_cte.c.min_rank == 1, ranked_cte.c.population))
                        ).label("min_pop"),
                        )
                        .group_by(ranked_cte.c.region_name)
                        .order_by(ranked_cte.c.region_name)
                    )
                
                result = await session.execute(stmt)
                return [dict(row._mapping) for row in result]
            except SQLAlchemyError:
                logger.exception("Failed to fetch aggregated data via ORM")
                raise