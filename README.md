# Crypto Risk API

A production-grade backend API for tracking cryptocurrency portfolios and computing
risk metrics. Built with FastAPI, PostgreSQL, and Docker.

## What This Is

A secured REST API that allows users to register, authenticate, manage crypto
portfolios, and track holdings. Designed as a foundation for a fintech-adjacent
portfolio risk management system.

## Tech Stack

| Technology | Purpose | Why |
|------------|---------|-----|
| FastAPI | Web framework | Async-native, automatic OpenAPI docs, Pydantic integration |
| PostgreSQL | Database | ACID guarantees, strong constraints, production-proven |
| SQLAlchemy 2.0 | ORM | Async support, type safety, migration tooling |
| Alembic | Migrations | Versioned schema changes, reversible, team-friendly |
| Docker | Containerization | Reproducible environments, easy local setup |
| argon2 | Password hashing | Winner of Password Hashing Competition, OWASP recommended |
| JWT (python-jose) | Authentication | Stateless, scalable, industry standard |
| slowapi | Rate limiting | Brute-force protection on auth endpoints |
| pytest + httpx | Testing | Async integration tests against real database |

## Architecture
HTTP Request
│
▼
Router (app/api/) ← HTTP only, no business logic
│
▼
Service (app/services/) ← Business logic, no HTTP awareness
│
▼
Repository (app/repositories/) ← Database access only
│
▼
PostgreSQL
## Local Setup

### Prerequisites
- Docker
- Python 3.12+
- uv (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 1. Clone and install dependencies
```bash
git clone https://github.com/650DataNerd/crypto-risk-api.git
cd crypto-risk-api
uv sync
```

### 2. Start PostgreSQL
```bash
docker run -d \
  --name crypto-risk-postgres \
  -e POSTGRES_USER=cryptouser \
  -e POSTGRES_PASSWORD=cryptopass \
  -e POSTGRES_DB=cryptorisk \
  -p 5432:5432 \
  -v crypto-risk-pgdata:/var/lib/postgresql/data \
  postgres:16
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Run migrations
```bash
uv run alembic upgrade head
```

### 5. Seed development data
```bash
PYTHONPATH=. uv run python scripts/seed.py
```

### 6. Start the server
```bash
uv run python -m uvicorn main:app --reload
```

API docs available at: http://127.0.0.1:8000/docs

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Register new user |
| POST | /auth/login | No | Login, returns JWT token |
| GET | /auth/me | Yes | Get current user profile |

### Portfolios
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /portfolios/ | Yes | List user's portfolios |
| POST | /portfolios/ | Yes | Create portfolio |

### Holdings
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /portfolios/{id}/holdings/ | Yes | List holdings |
| POST | /portfolios/{id}/holdings/ | Yes | Add holding |

## Running Tests
```bash
uv run pytest tests/ -v
```

## Security

- Passwords hashed with argon2id (OWASP recommended)
- JWT tokens expire after 30 minutes
- Login endpoint rate limited to 5 requests/minute per IP
- All routes require authentication except register and login
- Object-level authorization: users can only access their own data
- Security headers on every response (X-Frame-Options, HSTS, etc.)
- See [docs/threat-model.md](docs/threat-model.md) for full security analysis

## Documentation

- [Database Schema](docs/erd.md)
- [Threat Model](docs/threat-model.md)
