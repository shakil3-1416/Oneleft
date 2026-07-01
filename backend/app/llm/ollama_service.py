from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class OllamaService:
    def __init__(self) -> None:
        self.host = settings.OLLAMA_HOST.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    async def generate(
        self,
        *,
        system: str,
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "system": system,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.host}/api/generate",
                json=payload,
            )

        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except Exception:
            return False
