from __future__ import annotations

from abc import ABC, abstractmethod

from app.llm.ollama_service import OllamaService


class BaseAgent(ABC):
    name = "base_agent"
    system_prompt = "You are a helpful AI agent."

    def __init__(self) -> None:
        self.llm = OllamaService()

    @abstractmethod
    async def run(self, context: dict) -> dict:
        raise NotImplementedError

    async def ask(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
    ) -> str:
        return await self.llm.generate(
            system=self.system_prompt,
            prompt=prompt,
            temperature=temperature,
        )
