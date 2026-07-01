from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    store_id: int
    name: str
    email: EmailStr
    category: str


class CustomerResponse(BaseModel):
    id: int
    store_id: int
    name: str
    email: EmailStr
    category: str

    model_config = {
        "from_attributes": True
    }
