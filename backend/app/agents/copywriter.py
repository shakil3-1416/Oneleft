from __future__ import annotations

from app.agents.base import BaseAgent


class CopywriterAgent(BaseAgent):
    name = "copywriter_agent"
    system_prompt = """
You are the Copywriter Agent in OneLeft AI Marketing Workspace.

Your job:
- Write persuasive marketing content.
- Avoid spammy language.
- Keep copy clear, useful, and conversion-focused.
- Do not assume a specific industry unless given.
- Output clean markdown.
"""

    async def run(self, context: dict) -> dict:
        prompt = f"""
Write campaign assets using this strategy.

Strategy:
{context.get("strategy")}

Products:
{context.get("products")}

Return:
# Campaign Copy
## Email Subject Line
## Email Body
## Short SMS
## Facebook/Instagram Ad Copy
## LinkedIn/Post Copy
## Call To Action
"""
        context["copy"] = await self.ask(prompt, temperature=0.75)
        return context
