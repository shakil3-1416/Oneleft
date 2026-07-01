from __future__ import annotations

import time
from typing import Any

from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.strategy import StrategyAgent
from app.agents.copywriter import CopywriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.execution import ExecutionAgent


class WorkflowService:
    """
    Orchestrates the complete AI workflow.

    Future:
        - memory
        - tools
        - retries
        - streaming
        - parallel execution
    """

    def __init__(self) -> None:

        self.agents = [

            PlannerAgent(),

            ResearchAgent(),

            StrategyAgent(),

            CopywriterAgent(),

            ReviewerAgent(),

            ExecutionAgent(),

        ]

    async def run(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:

        context.setdefault("logs", [])

        workflow_start = time.perf_counter()

        for agent in self.agents:

            start = time.perf_counter()

            context = await agent.run(context)

            elapsed = round(
                time.perf_counter() - start,
                3,
            )

            context["logs"].append(
                {
                    "agent": agent.name,
                    "execution_time": elapsed,
                }
            )

        context["workflow_time"] = round(
            time.perf_counter() - workflow_start,
            3,
        )

        return context