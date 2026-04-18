# shopping-query-agent/tests/test_agent.py
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
import pytest
from app.agents.shopping_agent import ShoppingAgent
from app.models.request import ShoppingIntent


@pytest.mark.asyncio
async def test_shopping_agent_initialization() -> None:
    """
    Test that the ShoppingAgent can be initialized without errors.
    """
    # Mock adk.Agent to avoid real initialization/API calls
    with pytest.MonkeyPatch.context() as mp:
        mock_agent_class = MagicMock()
        mp.setattr("google.adk.Agent", mock_agent_class)
        
        agent = ShoppingAgent()
        assert agent is not None


@pytest.mark.asyncio
async def test_extract_intent_mocked() -> None:
    """
    Test extract_intent with a mocked ADK agent response.
    """
    with pytest.MonkeyPatch.context() as mp:
        mock_agent_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.data = ShoppingIntent(
            product_type="running shoes",
            brand="Nike",
            price_max=100.0
        )
        mock_agent_instance.run = AsyncMock(return_value=mock_response)
        
        # Patch adk.Agent to return our mock instance
        mp.setattr("google.adk.Agent", MagicMock(return_value=mock_agent_instance))
        
        agent = ShoppingAgent()
        intent = await agent.extract_intent("Find Nike shoes under $100")
        
        assert intent.product_type == "running shoes"
        assert intent.brand == "Nike"
        assert intent.price_max == 100.0
        mock_agent_instance.run.assert_called_once()
