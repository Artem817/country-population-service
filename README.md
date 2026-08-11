# Country Population Scraper

**Date:** August 10, 2026

## Technology Stack

- Python 3.11
- asyncio
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
├── print_data.py
├── requirements.txt
├── scrapers
│   ├── base.py
│   ├── factory.py
│   ├── stats_times.py
│   └── wiki.py
└── tests
    ├── test_factory.py
    └── test_scrapers.py
````

## Usage

### Start with the default source (Wikipedia)

```bash
docker-compose up get_data
docker-compose up print_data
```

### Launch with an additional source (StatisticsTimes)

```bash
DATA_SOURCE=stats docker-compose up get_data
docker-compose up print_data
```

> **Note regarding `stats` source:**
> You may have connection issues with this site. I recommend testing it in **GitHub Codespaces**, where network routing easily bypasses these regional restrictions.

## Testing

Run tests using pytest:

```bash
python -m pytest tests/ -v
```
