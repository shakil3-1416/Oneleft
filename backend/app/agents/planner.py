from __future__ import annotations

from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    name = "planner_agent"
    system_prompt = """
You are the Planner Agent in OneLeft AI Marketing Workspace.

Your job:
- Understand the campaign goal.
- Create a practical marketing plan.
- Do not assume a specific business domain.
- Output clean markdown.
"""

    async def run(self, context: dict) -> dict:
        prompt = f"""
Create a campaign plan.

Campaign:
{context.get("campaign_name")}

Store:
{context.get("store")}

Segment:
{context.get("segment")}

Products:
{context.get("products")}

Return:
# Campaign Plan
## Objective
## Target Audience
## Core Offer
## Recommended Channels
## Key Message
## Success Metrics
"""
        context["plan"] = await self.ask(prompt, temperature=0.5)
        return context
