# shopping-query-agent/tests/test_query_builder.py
from __future__ import annotations

import pytest
from app.models.request import ShoppingIntent
from app.services.query_builder import QueryBuilder


def test_query_builder_basic() -> None:
    """
    Verify basic query building with only product type.
    """
    builder = QueryBuilder()
    intent = ShoppingIntent(product_type="coffee maker")
    params = builder.build_params(intent)

    assert params["q"] == "coffee maker"
    assert "tbs" not in params


def test_query_builder_with_filters() -> None:
    """
    Verify query building with brand and price filters.
    """
    builder = QueryBuilder()
    intent = ShoppingIntent(
        product_type="running shoes",
        brand="Nike",
        price_min=50.0,
        price_max=150.0
    )
    params = builder.build_params(intent)

    assert "Nike" in params["q"]
    assert "ppr_min:50.0" in params["tbs"]
    assert "ppr_max:150.0" in params["tbs"]


def test_query_builder_attribute_filters() -> None:
    """
    Verify color and size are added to the search query.
    """
    builder = QueryBuilder()
    intent = ShoppingIntent(
        product_type="t-shirt",
        color="red",
        size="XL"
    )
    params = builder.build_params(intent)

    assert "red" in params["q"]
    assert "XL" in params["q"]
