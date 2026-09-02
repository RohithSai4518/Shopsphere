"""
Catalog Taxonomy and Attribute Validation Service for ShopSphere.
Provides schema validation and hierarchy checking across product categories.
"""

from typing import Dict, List, Any, Optional


class TaxonomyValidator:
    """
    Validates product category taxonomy and attribute specifications.
    """

    ALLOWED_CONDITIONS = {"NEW", "REFURBISHED", "USED_LIKE_NEW", "USED_GOOD"}
    ALLOWED_CURRENCIES = {"USD", "EUR", "GBP", "INR"}

    @classmethod
    def validate_category_attributes(cls, category_slug: str, attributes: Dict[str, Any]) -> List[str]:
        """
        Validate attribute dictionary against category requirements.
        Returns a list of validation error messages (empty if valid).
        """
        errors = []
        if not isinstance(attributes, dict):
            return ["Attributes payload must be a JSON object."]

        # Check required fields if any
        if not category_slug:
            errors.append("Category slug is required.")

        return errors

    @classmethod
    def sanitize_specifications(cls, specs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize and format technical specifications for catalog display.
        """
        if not isinstance(specs, dict):
            return {}
        sanitized = {}
        for key, value in specs.items():
            clean_key = str(key).strip().lower().replace(" ", "_")
            if isinstance(value, str):
                sanitized[clean_key] = value.strip()
            else:
                sanitized[clean_key] = value
        return sanitized
