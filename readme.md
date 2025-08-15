# BetterGroup - Backend Challenge

Index
- [Database Design Choices](/docs/db-diagram.md)
- [Technical Decisions](/docs/technical-decisions.md)
- [API Guidelines](#api-guidelines)
- [Quick Start](#quick-start)
- [Local Development](#local-development)

## Quick Start

### Clone and Setup

```bash
cp .env.example .env
```

### Start with Docker Compose
```bash
docker-compose up -d

docker-compose ps

docker-compose logs -f project_management_app
```

###  Initialize Database and Sync Data (if needed)
```bash
# Run database migrations
docker-compose exec project_management_app alembic upgrade head

# Sync users from external API
docker-compose exec project_management_app python fetch_and_populate.py
```


## Local Development
### Without Docker
```bash
# This creates .venv and installs the requirements.txt
source ~./init.sh # (By the way: i dont own this script, but its pretty helpful)

# Run migrations
alembic upgrade head

# Sync data with BetterGroup external API
python ./scripts/fetch_and_populate.py

# Start development server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
## API Guidelines

### API Authentication
All endpoints (except /docs, /redoc and /health) require API key authentication:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/companies
```