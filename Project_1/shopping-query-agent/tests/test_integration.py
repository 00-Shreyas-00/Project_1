# shopping-query-agent/tests/test_integration.py
from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_search_endpoint_integration_mocked() -> None:
    """
    Test the full /search flow with mocked agent and mocked SerpAPI results.
    """
    # Mock the ShoppingAgent.extract_intent
    mock_intent = MagicMock()
    mock_intent.product_type = "coffee maker"
    mock_intent.brand = None
    mock_intent.price_min = None
    mock_intent.price_max = None
    mock_intent.color = None
    mock_intent.size = None
    mock_intent.additional_filters = {}

    # Mock the whole agent's run methodology indirectly by mocking extract_intent
    with pytest.MonkeyPatch.context() as mp:
        # Since the router creates its own agent instance at module level (initially),
        # we need to be careful. In this case, routers/search.py initializes agent = ShoppingAgent().
        # We'll patch the agent INSTANCE in the search module.
        from app.routers import search
        search.agent.extract_intent = AsyncMock(return_value=mock_intent)
        
        # Also ensure SerpClient returns fake data to avoid network calls
        from app.models.response import ShoppingResult
        mock_results = [
            ShoppingResult(
                title="Mock Coffee Maker",
                link="http://example.com",
                price="$99.00",
                source="MockShop"
            )
        ]
        search.client.search_shopping = AsyncMock(return_value=mock_results)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"query": "I need a coffee maker"}
            )

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Mock Coffee Maker"
