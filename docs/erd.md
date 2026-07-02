# Database Schema — Crypto Risk API

## Entities

### User
| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | primary key |
| name | text | |
| email | text | unique |
| hashed_password | text | |
| is_active | boolean | default true |
| created_at | timestamp | auto |
| updated_at | timestamp | auto |

### Portfolio
| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | primary key |
| user_id | integer | FK → User.id, cascade delete |
| name | text | |
| created_at | timestamp | auto |
| updated_at | timestamp | auto |

### Holding
| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | primary key |
| portfolio_id | integer | FK → Portfolio.id, cascade delete |
| symbol | text | |
| amount | numeric | |
| created_at | timestamp | auto |
| updated_at | timestamp | auto |

### PriceSnapshot
| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | primary key |
| symbol | text | |
| price | numeric | |
| recorded_at | timestamp | auto |

## Relationships

- User has many Portfolios (one-to-many)
- Portfolio has many Holdings (one-to-many)
- PriceSnapshot is global market data, not tied to any user or portfolio

## Cascade Rules

- User deleted → all Portfolios deleted → all Holdings deleted
- Portfolio deleted → all Holdings deleted
