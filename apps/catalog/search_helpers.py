"""
Search and Facet Filtering Utilities for ShopSphere Storefront.
Provides query parsing, multi-attribute filtering, and pagination helpers.
"""

from typing import Dict, Any, List
from django.db.models import QuerySet, Q


class StorefrontSearchService:
    """
    Service helper for managing catalog search queries, facet counts, and sorting.
    """

    SORT_OPTIONS = {
        "price_asc": "price",
        "price_desc": "-price",
        "rating_desc": "-rating",
        "newest": "-created_at",
        "relevance": "-id",
    }

    @classmethod
    def apply_filters(
        cls,
        queryset: QuerySet,
        query: str = "",
        category_slug: str = "",
        min_price: float = None,
        max_price: float = None,
        sort_by: str = "relevance",
    ) -> QuerySet:
        """
        Filter queryset using standard search parameters.
        """
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if category_slug and category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        ordering = cls.SORT_OPTIONS.get(sort_by, "-id")
        return queryset.order_by(ordering)
