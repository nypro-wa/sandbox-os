from fastapi import FastAPI, HTTPException
from models import Item, ItemCreate

app = FastAPI(title="sandbox-os", version="0.1.0")

# In-memory store — replace with a real database when this grows
_items: dict[int, Item] = {}
_next_id = 1


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[Item]:
    return list(_items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@app.post("/items", status_code=201)
def create_item(body: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **body.model_dump())
    _items[_next_id] = item
    _next_id += 1
    # TODO: persist to database
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
