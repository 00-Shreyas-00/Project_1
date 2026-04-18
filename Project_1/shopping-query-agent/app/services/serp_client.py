# shopping-query-agent/app/services/serp_client.py
from __future__ import annotations

import httpx
from app.config import settings
from app.models.response import ShoppingResult, SearchResponse


class SerpClient:
    """
    Client for interacting with the SerpAPI Google Shopping engine.
    Supports both real API calls and mock responses for testing.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.SERP_API_KEY
        self.base_url = "https://serpapi.com/search"

    async def search_shopping(self, params: dict[str, str | int | float | None]) -> list[ShoppingResult]:
        """
        Executes a Google Shopping search via SerpAPI.
        If no real API key is present, returns a mock response.
        """
        if not self.api_key or self.api_key == "dummy_val":
            return self._get_mock_response()

        request_params = {
            "engine": "google_shopping",
            "api_key": self.api_key,
            "gl": "us",
            "hl": "en",
            **{k: str(v) for k, v in params.items() if v is not None},
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.base_url, params=request_params)
            response.raise_for_status()
            data = response.json()

        results = []
        shopping_results = data.get("shopping_results", [])
        for item in shopping_results:
            results.append(
                ShoppingResult(
                    title=item.get("title", "Unknown Product"),
                    price=item.get("price", "N/A"),
                    link=item.get("link", "#"),
                    thumbnail=item.get("thumbnail"),
                    source=item.get("source"),
                )
            )

        return results

    def _get_mock_response(self) -> list[ShoppingResult]:
        """
        Returns a hardcoded list of ShoppingResult objects for testing.
        """
        return [
            ShoppingResult(
                title="Mock Product A",
                price="$99.99",
                link="https://example.com/a",
                thumbnail="https://example.com/a.jpg",
                source="Mock Store",
            ),
            ShoppingResult(
                title="Mock Product B",
                price="$45.00",
                link="https://example.com/b",
                thumbnail="https://example.com/b.jpg",
                source="Mock Shop",
            ),
        ]
