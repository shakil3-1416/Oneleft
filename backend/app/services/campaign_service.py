from __future__ import annotations

import inspect
import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.store import Store
from app.models.product import Product
from app.models.segment import Segment
from app.workflow.workflow_service import WorkflowService


class CampaignService:
    def __init__(self, db: Session):
        self.db = db

    def list_campaigns(self, skip: int = 0, limit: int = 100) -> list[Campaign]:
        stmt = select(Campaign).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_campaign(self, campaign_id: int) -> Campaign:
        campaign = self.db.get(Campaign, campaign_id)
        if campaign is None:
            raise LookupError("Campaign not found")
        return campaign

    def create_campaign(self, data: dict[str, Any]) -> Campaign:
        payload = self._clean_payload(data)
        campaign = Campaign(**payload)
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def update_campaign(self, campaign_id: int, data: dict[str, Any]) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        payload = self._clean_payload(data, partial=True)

        for key, value in payload.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)

        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def delete_campaign(self, campaign_id: int) -> None:
        campaign = self.get_campaign(campaign_id)
        self.db.delete(campaign)
        self.db.commit()

    def generate_campaign(self, campaign_id: int) -> Campaign:
        campaign = self.get_campaign(campaign_id)

        store = self.db.get(Store, getattr(campaign, "store_id", None))
        product = self.db.get(Product, getattr(campaign, "product_id", None))
        segment = self.db.get(Segment, getattr(campaign, "segment_id", None))

        context = {
            "campaign": self._model_to_dict(campaign),
            "store": self._model_to_dict(store),
            "product": self._model_to_dict(product),
            "segment": self._model_to_dict(segment),
            "instruction": (
                "Generate a business-agnostic marketing campaign. "
                "Do not assume the business is a clothing store. "
                "Ignore rule_json. Use the available store, product, segment, "
                "and campaign fields only."
            ),
        }

        workflow = self._build_workflow()
        result = self._run_workflow(workflow, context)

        if hasattr(campaign, "generated_content"):
            setattr(campaign, "generated_content", self._serialize_generated_content(result))

        if hasattr(campaign, "status"):
            setattr(campaign, "status", "generated")

        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def _build_workflow(self) -> WorkflowService:
        try:
            return WorkflowService(db=self.db)
        except TypeError:
            try:
                return WorkflowService(self.db)
            except TypeError:
                return WorkflowService()

    def _run_workflow(self, workflow: WorkflowService, context: dict[str, Any]) -> Any:
        candidate_methods = (
            "run",
            "execute",
            "generate",
            "generate_campaign",
            "run_campaign",
            "run_workflow",
        )

        for method_name in candidate_methods:
            method = getattr(workflow, method_name, None)
            if not callable(method):
                continue

            try:
                signature = inspect.signature(method)
                params = signature.parameters

                if len(params) == 0:
                    return method()

                if "context" in params:
                    return method(context=context)

                if "campaign_context" in params:
                    return method(campaign_context=context)

                if "campaign" in params:
                    return method(
                        campaign=context["campaign"],
                        store=context["store"],
                        product=context["product"],
                        segment=context["segment"],
                    )

                return method(context)
            except TypeError:
                continue

        raise RuntimeError("WorkflowService has no supported execution method.")

    def _clean_payload(self, data: dict[str, Any], partial: bool = False) -> dict[str, Any]:
        if hasattr(data, "model_dump"):
            data = data.model_dump(exclude_unset=partial)
        elif not isinstance(data, dict):
            data = dict(data)

        ignored = {"id", "created_at", "updated_at"}
        payload = {}

        for key, value in data.items():
            if key in ignored:
                continue
            if key == "rule_json":
                payload[key] = value
                continue
            if hasattr(Campaign, key):
                payload[key] = value

        return payload

    def _model_to_dict(self, obj: Any) -> dict[str, Any]:
        if obj is None:
            return {}

        result = {}
        for column in obj.__table__.columns:
            key = column.name
            if key == "rule_json":
                continue
            result[key] = getattr(obj, key)

        return result

    def _serialize_generated_content(self, result: Any) -> Any:
        if isinstance(result, str):
            return result

        try:
            return json.dumps(result, ensure_ascii=False, default=str)
        except TypeError:
            return str(result)
