from pydantic import BaseModel, field_validator


class ItemCreate(BaseModel):
    name: str
    description: str = ""

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        # Reject empty or whitespace-only names; a valid name is kept as sent.
        if not value.strip():
            raise ValueError("name must not be empty")
        return value


class Item(ItemCreate):
    id: int
