from __future__ import annotations

from app.agents.base import BaseAgent


class ReviewerAgent(BaseAgent):
    name = "reviewer_agent"
    system_prompt = """
You are the Reviewer Agent in OneLeft AI Marketing Workspace.

Your job:
- Review campaign copy.
- Improve clarity, persuasion, and professionalism.
- Remove weak or generic wording.
- Keep the final copy practical.
- Output clean markdown.
"""

    async def run(self, context: dict) -> dict:
        prompt = f"""
Review and improve this campaign copy.

Copy:
{context.get("copy")}

Strategy:
{context.get("strategy")}

Return:
# Reviewed Campaign Copy
## Review Notes
## Improved Email Subject Line
## Improved Email Body
## Improved SMS
## Improved Social Ad Copy
## Improved LinkedIn/Post Copy
## Final CTA
"""
        context["review"] = await self.ask(prompt, temperature=0.45)
        return context
