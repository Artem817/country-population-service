from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class CountryPopulation(Base):
    """ ORM model representing country population records.
    """
    __tablename__ = "countries_population"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_name : Mapped[str] = mapped_column(String(255), nullable=False)
    region_name : Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    population: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source : Mapped[str] = mapped_column(String(50), nullable=False,default="wiki")
    
    def __repr__(self) -> str:
        """Return a string repr"""
        return ( f"<CountryPopulation(country='{self.country_name}', " f"region='{self.region_name}', population={self.population})>" )