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
- `GET /items/{id}` — get one item
- `POST /items` — create an item
- `DELETE /items/{id}` — delete an item
