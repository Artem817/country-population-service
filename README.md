# Country Population Scraper

**Date:** August 10, 2026

## Technology Stack

- Python 3.11
- Asyncio
- SQLAlchemy Async ORM
- asyncpg
- PostgreSQL 15
- BeautifulSoup4
- aiohttp
- Docker
- Docker Compose

## Project Structure

```text
.
├── Dockerfile
├── README.md
├── db.py
├── docker-compose.yml
├── get_data.py
├── logger.py
├── models.py
├── note.txt
├── print_data.py
├── requirements.txt
└── scrapers
    ├── base.py
    ├── factory.py
    └── wiki.py

### Start with default source (Wikipedia))
```bash
docker-compose up get_data
docker-compose up print_data

### Launch with additional source (StatisticsTimes)
```bash
DATA_SOURCE=stats docker-compose up get_data
docker-compose up print_data

### Run tests using pytest:
```bash
python -m pytest tests/ -v