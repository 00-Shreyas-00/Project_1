# shopping-query-agent/app/models/response.py
from __future__ import annotations

from pydantic import BaseModel, Field


class ShoppingResult(BaseModel):
    """
    Normalized product result from SerpAPI Google Shopping.
    """

    title: str = Field(..., description="Product title")
    price: str = Field(..., description="Formatted price string")
    link: str = Field(..., description="Direct link to the product")
    thumbnail: str | None = Field(None, description="URL of the product thumbnail image")
    source: str | None = Field(None, description="The merchant or source of the product")


class SearchResponse(BaseModel):
    """
    Schema for the search API response.
    """

    results: list[ShoppingResult] = Field(default_factory=list, description="List of normalized shopping results")
