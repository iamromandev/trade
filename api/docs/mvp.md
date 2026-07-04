# Minimal Paper Trading MVP Plan

## Goal

Let users trade stocks with virtual money using real market data, with the simplest possible implementation.

## Scope (MVP)

### Phase 1 — Foundation

| Feature | Details |
|---|---|
| **Virtual Wallet** | Each user gets $100K virtual USD on signup; persist balance |
| **Portfolio** | Track positions (ticker, shares, avg cost); no short selling |
| **Market Data** | Fetch real-time + historical prices via a free API (e.g., yfinance, Finnhub, or Twelve Data) |
| **Order Entry** | `POST /api/v1/trade/orders` — market buy/sell only (no limit/stop) |
| **Basic P&L** | Endpoint returning portfolio value = cash + positions × current price |
| **Trade History** | Simple ledger of executed orders per user |

### Phase 2 (Post-MVP)

Limit/stop orders, watchlists, P&L charts, leaderboards, paper trading competitions.

## API Endpoints

```
GET  /api/v1/trade/quote/{symbol}        → current price + basic info
GET  /api/v1/trade/portfolio             → positions + total value + cash
POST /api/v1/trade/orders                → place market order
GET  /api/v1/trade/orders                → order history
GET  /api/v1/trade/orders/{id}           → order detail
```

## Database Models (new `trade` module)

- **`Wallet`** — user_id, balance (Decimal), created_at
- **`Position`** — user_id, symbol, quantity, avg_price
- **`Order`** — user_id, symbol, side (buy/sell), quantity, price, status (filled/rejected), created_at

## Architecture

```
src/module/trade/
├── __init__.py
├── router.py        # API routes
├── schema.py        # Pydantic request/response schemas
├── service.py       # Business logic (place order, calc P&L)
├── repository.py    # DB access (Wallet, Position, Order)
├── client.py        # External market data client
└── model.py         # Tortoise ORM models
```

Follows the existing pattern in `src/module/health/` and `user/`.

## Key Design Decisions (MVP)

1. **Market orders only** — price = market price at time of execution
2. **No fractional shares** — whole shares only
3. **No margin/leverage** — must have sufficient cash to buy
4. **No short selling** — can only sell what you own
5. **Synchronous execution** — order fills immediately at current price (vs. async matching engine)
6. **Market data** — external API called synchronously; cache quotes for 1 min to avoid rate limits
7. **No WebSocket** — REST-only for MVP

## Non-Goals (explicitly excluded from MVP)

- Real-time streaming prices / WebSocket feeds
- Complex order types (limit, stop, trailing stop)
- Short selling, margin, options, futures
- Tax lot accounting (FIFO/LIFO)
- Admin back-office / trade settlement
- User-facing charts (deferred)
- Multiple currency / international markets

## Dependencies to add

- `httpx` or `aiohttp` — for external market data API calls
- Data provider client library (e.g., `yfinance` or similar)
