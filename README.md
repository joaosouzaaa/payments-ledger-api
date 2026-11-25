# Payments Ledger API

A payments ledger built with FastAPI, async SQLAlchemy 2.0 and PostgreSQL.
Uses synthetic data only.

> Work in progress. Status: savings accounts (create, get, close, paged list).
> Next: transactions, entries, idempotency, reversals.

## Run

```powershell
docker compose up --build
```

API docs: http://localhost:8000/docs

## Test

```powershell
docker compose run --rm api sh -c "uv sync --group dev && pytest"
```

## License

[MIT](LICENSE)
