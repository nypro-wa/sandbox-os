# sandbox-os

A minimal FastAPI service used as the pilot project for the Personal AI Manager system.
Its purpose is to serve as a realistic but simple codebase for testing the analyst worker,
the register-project playbook, and the Phase 3 delivery loop.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

- `GET /health` — health check
- `GET /items` — list all items
- `GET /items/count` — number of items, as `{"count": <n>}`
- `GET /items/{id}` — get one item
- `POST /items` — create an item
- `DELETE /items/{id}` — delete an item

## Testing

Tests live in `tests/` and use pytest with FastAPI's `TestClient`. Install the test
dependencies with `pip install -r requirements-dev.txt`, then run from the repository root:

```bash
/home/sesq/Projects/companion-os/sandbox-os/.venv/bin/python -m pytest -q
```

With any other environment that has the test dependencies, `python -m pytest -q` does the same.
Each test starts from an empty store: an autouse fixture resets `main._items` and `main._next_id`.
