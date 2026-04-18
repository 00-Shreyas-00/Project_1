# shopping-query-agent/app/agents/shopping_agent.py
from __future__ import annotations

from typing import Optional
import logging
from google.adk import Agent, Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.utils.context_utils import Aclosing
from google.genai import types

from app.models.request import ShoppingIntent
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = """
You are a helpful shopping assistant. Your task is to extract structured shopping intent from a user's natural language query.
Extract the following information:
- product_type: The main item they are looking for (e.g., "shoes", "laptop").
- brand: Any specific brand mentioned (e.g., "Nike", "Apple").
- min_price: Minimum price if mentioned.
- max_price: Maximum price if mentioned.
- color: Preferred color if mentioned.
- size: Preferred size if mentioned.
- additional_filters: Any other relevant keywords as a single string (e.g., "wireless running").

Always return a valid ShoppingIntent structured response.
"""


class ShoppingAgent:
    """
    Agent that utilizes Google ADK to process shopping queries.
    """

    def __init__(self) -> None:
        # Define the agent with an output schema and key
        self.agent = Agent(
            name="ShoppingAgent",
            model="gemini-1.5-flash",
            instruction=SYSTEM_INSTRUCTIONS,
            output_schema=ShoppingIntent,
            output_key="intent"  # This tells ADK where to store the validated result
        )
        
        # We need a session service and a runner to execute the agent in ADK 2.0
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="ShoppingApp",
            agent=self.agent,
            session_service=self.session_service
        )

    async def extract_intent(self, query: str) -> ShoppingIntent:
        """
        Extracts structured ShoppingIntent from a natural language query 
        using the Google ADK Agent and Runner.
        """
        user_id = "default_user"
        session_id = "initial_session"
        
        try:
            # Create a session if it doesn't exist
            session = await self.session_service.get_session(
                app_name="ShoppingApp", 
                user_id=user_id, 
                session_id=session_id
            )
            if not session:
                session = await self.session_service.create_session(
                    app_name="ShoppingApp", 
                    user_id=user_id, 
                    session_id=session_id
                )

            # Prepare the user message
            new_message = types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )

            # Run the agent through the runner
            async with Aclosing(
                self.runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=new_message
                )
            ) as agen:
                async for event in agen:
                    # We process events as they come, though for intent extraction 
                    # we mainly care about the final state.
                    pass

            # After the run, the validated result should be in the session state 
            # under the 'output_key' we defined.
            updated_session = await self.session_service.get_session(
                app_name="ShoppingApp", 
                user_id=user_id, 
                session_id=session_id
            )
            
            intent_data = updated_session.state.get("intent")
            if not intent_data:
                # Fallback or error if no intent was extracted
                logger.warning(f"No intent extracted for query: {query}")
                return ShoppingIntent(product_type=query)
            
            # If intent_data is already a dict or ShoppingIntent, return it
            if isinstance(intent_data, ShoppingIntent):
                return intent_data
            return ShoppingIntent.model_validate(intent_data)

        except Exception as e:
            logger.error(f"Error during intent extraction: {e}")
            # Return a basic intent as a fallback to allow the search to proceed
            return ShoppingIntent(product_type=query)
