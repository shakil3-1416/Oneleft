from __future__ import annotations

from app.agents.base import BaseAgent


class ResearchAgent(BaseAgent):
    name = "research_agent"
    system_prompt = """
You are the Research Agent in OneLeft AI Marketing Workspace.

Your job:
- Generate business-agnostic market assumptions.
- Identify likely customer pain points.
- Identify opportunity angles.
- Do not claim real-time web research.
- Output clean markdown.
"""

    async def run(self, context: dict) -> dict:
        prompt = f"""
Based on this campaign plan, produce research insights.

Campaign Plan:
{context.get("plan")}

Business Context:
{context.get("store")}

Products:
{context.get("products")}

Return:
# Research Insights
## Audience Assumptions
## Customer Pain Points
## Buying Motivations
## Market Opportunities
## Messaging Risks
"""
        context["research"] = await self.ask(prompt, temperature=0.6)
        return context
