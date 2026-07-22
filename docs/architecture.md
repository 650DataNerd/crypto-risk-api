# Architecture — Crypto Risk API

## System Overview
┌─────────────────┐
                │   HTTP Client   │
                └────────┬────────┘
                         │ HTTPS
                         ▼
                ┌─────────────────┐
                │   FastAPI App   │
                │                 │
                │  ┌───────────┐  │
                │  │  Routers  │  │
                │  └─────┬─────┘  │
                │        │        │
                │  ┌─────▼─────┐  │
                │  │ Services  │  │
                │  └─────┬─────┘  │
                │        │        │
                │  ┌─────▼─────┐  │
                │  │   Repos   │  │
                │  └─────┬─────┘  │
                └────────┼────────┘
                         │
             ┌───────────┴───────────┐
             │                       │
    ┌────────▼────────┐   ┌──────────▼──────────┐
    │   PostgreSQL    │   │       Redis          │
    │                 │   │                      │
    │ - users         │   │ - portfolios:{id}    │
    │ - portfolios    │   │ - price:{symbol}     │
    │ - holdings      │   │                      │
    │ - price_snapshot│   │  TTL: 60-120 seconds │
    └─────────────────┘   └──────────────────────┘
                                     ▲
                          ┌──────────┴──────────┐
                          │  Background Worker  │
                          │                     │
                          │ - runs every 60s    │
                          │ - fetches prices    │
                          │   from CoinGecko    │
                          │ - stores in Postgres│
                          │ - caches in Redis   │
                          └─────────────────────┘
## Components

### FastAPI Application
The main HTTP server handling all API requests. Organized in three layers:
- **Routers** (`app/api/`) — HTTP request/response only, no business logic
- **Services** (`app/services/`) — business logic, no HTTP awareness
- **Repositories** (`app/repositories/`) — database access only

### PostgreSQL
Primary data store for all persistent data. Used for:
- User accounts and credentials
- Portfolio and holding records
- Historical price snapshots for risk metric computation

### Redis
In-memory cache for fast reads. Used for:
- Portfolio lists per user (TTL: 60s, invalidated on write)
- Latest crypto prices (TTL: 120s, updated by worker)
- Falls back gracefully to Postgres if unavailable

### Background Worker
Async task running inside the FastAPI process. Runs every 60 seconds to:
- Fetch BTC and ETH prices from CoinGecko API
- Store snapshots in PostgreSQL for historical risk analysis
- Cache latest prices in Redis for instant portfolio valuation

## Key Design Decisions

### Layered Architecture
Business logic lives in services, not routes. This enables unit testing
of logic without spinning up an HTTP server, and allows the same service
to be called from routes, background jobs, or CLI scripts.

### Cache-Aside Pattern
The application controls caching explicitly. On read: check cache first,
fall back to database. On write: invalidate the relevant cache key.
This avoids stale data while keeping the implementation simple.

### Async Throughout
All I/O operations (database, Redis, external HTTP) are async. This allows
the single-process server to handle many concurrent requests efficiently
without threads.

### Repository Pattern
All database queries are isolated in repository classes. If the database
changes (different table structure, different ORM), only repositories
change — services and routes are unaffected.

## Known Limitations

- Background worker runs in the same process as the API — a worker crash
  affects the API. Production fix: separate Docker container.
- Redis client creates a new connection per request — connection pooling
  would improve performance under high load.
- Rate limiting is in-memory — distributed deployments need Redis-backed
  rate limiting.
