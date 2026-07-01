from pydantic import BaseModel, EmailStr


class StoreCreate(BaseModel):
    name: str
    owner_email: EmailStr
    subscription_plan: str = "free"


class StoreResponse(BaseModel):
    id: int
    name: str
    owner_email: EmailStr
    subscription_plan: str

    model_config = {
        "from_attributes": True
    }
