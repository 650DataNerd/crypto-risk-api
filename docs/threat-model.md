# Threat Model — Crypto Risk API

## Overview

This document identifies potential security threats to the Crypto Risk API,
assesses their impact, and describes the controls in place to mitigate them.

---

## Assets

- User credentials (email, hashed passwords)
- JWT tokens (access to user data)
- Portfolio and holding data (financial information)
- Database (all application data)
- SECRET_KEY (used to sign all tokens)

---

## Threat 1: Credential Brute Force

**Attack:** An attacker repeatedly attempts to guess a user's password
via the login endpoint.

**Impact:** High — successful attack gives full account access.

**Controls:**
- argon2 password hashing makes each verification slow (~100ms),
  limiting attempts to ~10/second per thread
- Rate limiting on /auth/login: 5 attempts per minute per IP
- Same error message for wrong email and wrong password prevents
  email enumeration

**Residual risk:** Distributed attacks from many IPs bypass per-IP
rate limiting. Mitigation: move rate limit counter to Redis (planned Week 4).

---

## Threat 2: Token Forgery

**Attack:** An attacker modifies a JWT payload to impersonate another user
(e.g. changing "sub": "3" to "sub": "1").

**Impact:** Critical — gives access to any user's data.

**Controls:**
- JWT signature verified on every request using SECRET_KEY
- Modified tokens produce a signature mismatch and are rejected with 401
- SECRET_KEY is a 256-bit random value, never committed to git

**Residual risk:** If SECRET_KEY is leaked, all tokens can be forged.
Mitigation: SECRET_KEY stored only in .env (gitignored) and server
environment variables, never in code.

---

## Threat 3: Broken Object-Level Authorization

**Attack:** An authenticated user accesses another user's portfolios or
holdings by guessing or manipulating resource IDs.

**Impact:** High — exposes other users' financial data.

**Controls:**
- Every portfolio query filters by both portfolio ID and the authenticated
  user's ID extracted from the JWT token
- A valid token for user 3 cannot access portfolios owned by user 1,
  even with a correct portfolio ID
- Tests explicitly verify cross-user isolation

**Residual risk:** None identified with current implementation.

---

## Threat 4: SQL Injection

**Attack:** An attacker injects malicious SQL via API input fields.

**Impact:** Critical — could expose or destroy all data.

**Controls:**
- All database queries use SQLAlchemy parameterized queries
- User input never interpolated directly into SQL strings
- Pydantic validates and rejects malformed input before it reaches
  the database layer

**Residual risk:** None identified with current implementation.

---

## Threat 5: Sensitive Data Exposure

**Attack:** API responses accidentally include sensitive fields such as
hashed_password, or secrets are committed to git.

**Impact:** High — hashed passwords enable offline cracking attacks.

**Controls:**
- UserResponse schema explicitly excludes hashed_password
- FastAPI response_model strips any fields not in the schema
- .env is gitignored from commit 1
- SECRET_KEY, DATABASE_URL, and passwords never appear in committed files
- pip-audit/safety scans planned for CI (Week 5)

**Residual risk:** Developer error could introduce a new schema that
accidentally exposes fields. Mitigation: code review via PR process.

---

## Threat 6: Token Theft

**Attack:** An attacker intercepts a JWT token in transit or from logs.

**Impact:** High — stolen token gives full account access until expiry.

**Controls:**
- Tokens expire after 30 minutes (ACCESS_TOKEN_EXPIRE_MINUTES)
- Tokens transmitted via Authorization header, not URL query parameters
- HTTPS enforced in production (planned Week 7)

**Residual risk:** 30-minute window remains after theft. Mitigation:
refresh token rotation and token revocation list (future enhancement).

---

## What Is Not Yet Implemented

- Refresh tokens
- Token revocation
- Account lockout after N failed attempts
- HTTPS (planned Week 7)
- Redis-backed rate limiting (planned Week 4)
- Dependency vulnerability scanning in CI (planned Week 5)
