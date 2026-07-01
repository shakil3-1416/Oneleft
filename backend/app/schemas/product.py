from pydantic import BaseModel


class ProductCreate(BaseModel):
    store_id: int
    name: str
    category: str
    price: float
    description: str
    inventory_count: int


class ProductResponse(BaseModel):
    id: int
    store_id: int
    name: str
    category: str
    price: float
    description: str
    inventory_count: int

    model_config = {
        "from_attributes": True
    }
