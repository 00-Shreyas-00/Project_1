# shopping-query-agent/app/models/request.py
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class SearchRequest(BaseModel):
    """
    Schema for the incoming shopping search request.
    """

    query: str = Field(..., description="The natural language shopping query from the user.")


class ShoppingIntent(BaseModel):
    """
    Structured shopping intent extracted from natural language.
    Strictly follows Gemini's JSON Schema requirements (no additionalProperties).
    """
    model_config = ConfigDict(extra='forbid')

    product_type: str = Field(..., description="The type of product being searched for.")
    brand: str | None = Field(None, description="Preferred brand.")
    price_min: float | None = Field(None, description="Minimum price.")
    price_max: float | None = Field(None, description="Maximum price.")
    color: str | None = Field(None, description="Preferred color.")
    size: str | None = Field(None, description="Preferred size.")
    additional_filters: str | None = Field(None, description="Any other specific filters or keywords.")
