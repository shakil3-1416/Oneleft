from pydantic import BaseModel


class CampaignCreate(BaseModel):
    store_id: int
    segment_id: int
    name: str


class CampaignUpdate(BaseModel):
    store_id: int | None = None
    segment_id: int | None = None
    name: str | None = None
    status: str | None = None


class CampaignResponse(BaseModel):
    id: int
    store_id: int
    segment_id: int
    name: str
    status: str
    generated_content: str | None

    model_config = {
        "from_attributes": True
    }


class CampaignGenerateResponse(BaseModel):
    campaign_id: int
    generated_content: str


class CampaignPreviewResponse(BaseModel):
    campaign_id: int
    generated_content: str | None