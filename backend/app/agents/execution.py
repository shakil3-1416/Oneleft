from __future__ import annotations

from app.agents.base import BaseAgent


class ExecutionAgent(BaseAgent):
    name = "execution_agent"
    system_prompt = """
You are the Execution Agent in OneLeft AI Marketing Workspace.

Your job:
- Package the final campaign into a clean execution-ready format.
- Output markdown only.
"""

    async def run(self, context: dict) -> dict:
        final = f"""
# OneLeft AI Marketing Campaign

## Campaign
{context.get("campaign_name")}

## Planner Output
{context.get("plan")}

## Research Output
{context.get("research")}

## Strategy Output
{context.get("strategy")}

## Final Reviewed Copy
{context.get("review")}
""".strip()

        context["final"] = final
        return context
