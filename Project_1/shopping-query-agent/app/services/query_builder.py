# shopping-query-agent/app/services/query_builder.py
from __future__ import annotations

from app.models.request import ShoppingIntent


class QueryBuilder:
    """
    Builds SerpAPI parameters from a structured ShoppingIntent.
    """

    def build_params(self, intent: ShoppingIntent) -> dict[str, str | int | float]:
        """
        Maps ShoppingIntent fields to SerpAPI Google Shopping parameters.
        """
        # Base query string
        query_parts = [intent.product_type]
        if intent.brand:
            query_parts.append(intent.brand)
        if intent.color:
            query_parts.append(intent.color)
        if intent.size:
            query_parts.append(intent.size)

        # Add additional filters to the query string if present
        if intent.additional_filters:
            query_parts.append(intent.additional_filters)

        q = " ".join(query_parts)

        # Build tbs (to be searched) parameter for filters like price
        tbs_parts = []
        if intent.price_min is not None:
            tbs_parts.append(f"ppr_min:{intent.price_min}")
        if intent.price_max is not None:
            tbs_parts.append(f"ppr_max:{intent.price_max}")
        
        params: dict[str, str | int | float] = {
            "q": q,
            "engine": "google_shopping",
            "gl": "us",
            "hl": "en",
        }

        if tbs_parts:
            params["tbs"] = ",".join(tbs_parts)

        return params
