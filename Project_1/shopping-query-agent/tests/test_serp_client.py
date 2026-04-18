# shopping-query-agent/tests/test_serp_client.py
from __future__ import annotations

import pytest
from app.services.serp_client import SerpClient


@pytest.mark.asyncio
async def test_serp_client_mock_mode() -> None:
    """
    Verify that SerpClient returns mock data when api_key is 'dummy_val'.
    """
    client = SerpClient(api_key="dummy_val")
    response = await client.search_shopping({"q": "coffee maker"})

    assert len(response.results) > 0
    assert response.results[0].title.startswith("Mock")
