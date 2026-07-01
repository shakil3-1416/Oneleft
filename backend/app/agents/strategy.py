from __future__ import annotations

from app.agents.base import BaseAgent


class StrategyAgent(BaseAgent):
    name = "strategy_agent"
    system_prompt = """
You are the Strategy Agent in OneLeft AI Marketing Workspace.

Your job:
- Convert plan and research into a campaign strategy.
- Make it usable for copywriting.
- Keep it business-agnostic.
- Output clean markdown.
"""

    async def run(self, context: dict) -> dict:
        prompt = f"""
Create a campaign strategy from the plan and research.

Plan:
{context.get("plan")}

Research:
{context.get("research")}

Return:
# Campaign Strategy
## Positioning
## Main Promise
## Offer Angle
## Messaging Pillars
## Tone of Voice
## CTA Strategy
"""
        context["strategy"] = await self.ask(prompt, temperature=0.6)
        return context
