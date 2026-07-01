from pydantic import BaseModel


class SegmentCreate(BaseModel):
    store_id: int
    name: str
    description: str
    rule_json: str


class SegmentResponse(BaseModel):
    id: int
    store_id: int
    name: str
    description: str
    rule_json: str

    model_config = {
        "from_attributes": True
    }
