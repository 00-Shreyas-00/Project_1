from fastapi import APIRouter, HTTPException
from app.models.request import SearchRequest
from app.models.response import SearchResponse
from app.agents.shopping_agent import ShoppingAgent
from app.services.query_builder import QueryBuilder
from app.services.serp_client import SerpClient

router = APIRouter()

# Initialize components
agent = ShoppingAgent()
builder = QueryBuilder()
client = SerpClient()

@router.post("/search", response_model=SearchResponse)
async def perform_search(request: SearchRequest):
    """
    Main endpoint for processing natural language shopping queries.
    """
    try:
        # 1. Extract structured intent using the Google ADK Agent
        intent = await agent.extract_intent(request.query)
        
        # 2. Convert structured intent into SerpAPI parameters
        params = builder.build_params(intent)
        
        # 3. Perform the search using SerpAPI (or mock data if unconfigured)
        results = await client.search_shopping(params)
        
        return SearchResponse(results=results)
    except Exception as e:
        # Wrap and raise exceptions as HTTP 500 errors
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
