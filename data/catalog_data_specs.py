"""
Extended Data Specifications Module for ShopSphere Product Catalog.
Provides structured taxonomy schemas, validation helpers, domain specifications,
and search indexing data structures for catalog management.
"""

from typing import List, Dict, Any, Optional

CATALOG_METADATA_VERSION = "2.4.0"

TAXONOMY_TREE = {
    "electronics": {
        "title": "Electronics & Consumer Gadgets",
        "subcategories": ["projectors", "drones", "power-banks", "vr-headsets"],
        "attribute_keys": ["lumens", "battery", "resolution", "weight"]
    },
    "smartphones": {
        "title": "Mobiles & Smartphones",
        "subcategories": ["5g-phones", "tablets", "foldables", "accessories"],
        "attribute_keys": ["screen_size", "storage", "camera_mp", "ram"]
    },
    "laptops": {
        "title": "Laptops & Computers",
        "subcategories": ["ultrabooks", "workstations", "mini-pcs", "desktops"],
        "attribute_keys": ["cpu_cores", "ram_gb", "ssd_storage", "gpu"]
    },
    "audio-headphones": {
        "title": "Headphones & Audio",
        "subcategories": ["anc-headphones", "wireless-earbuds", "speakers", "monitors"],
        "attribute_keys": ["battery_hours", "driver_mm", "ip_rating", "anc"]
    },
    "smartwatches": {
        "title": "Smartwatches & Wearables",
        "subcategories": ["health-trackers", "titanium-watches", "gps-sports-watches"],
        "attribute_keys": ["sensors", "water_resistance", "glass_type", "strap_material"]
    },
    "clothing": {
        "title": "Clothing & Apparel",
        "subcategories": ["jackets", "hoodies", "shirts", "jeans"],
        "attribute_keys": ["size", "color", "fabric_type", "waterproof_rating"]
    },
    "shoes": {
        "title": "Shoes & Footwear",
        "subcategories": ["running-shoes", "marathon-racers", "oxford-shoes", "sneakers"],
        "attribute_keys": ["size", "color", "midsole_foam", "drop_mm"]
    },
    "bags-accessories": {
        "title": "Bags & Accessories",
        "subcategories": ["daypacks", "briefcases", "travel-duffels", "sunglasses"],
        "attribute_keys": ["volume_liters", "material", "laptop_compartment", "uv_rating"]
    },
    "home-kitchen": {
        "title": "Home & Kitchen",
        "subcategories": ["espresso-makers", "cookware", "air-purifiers", "blenders"],
        "attribute_keys": ["power_watts", "capacity_liters", "material", "hepa_rating"]
    },
    "beauty": {
        "title": "Beauty & Personal Care",
        "subcategories": ["skincare-kits", "facial-brushes", "perfumes", "trimmers"],
        "attribute_keys": ["skin_type", "active_ingredients", "battery_runtime", "volume_ml"]
    },
    "sports": {
        "title": "Sports & Fitness",
        "subcategories": ["yoga-mats", "dumbbells", "exercise-bikes", "water-bottles"],
        "attribute_keys": ["weight_lbs", "thickness_mm", "resistance_type", "material"]
    },
    "books": {
        "title": "Books & Media",
        "subcategories": ["cookbooks", "tech-handbooks", "design-guides"],
        "attribute_keys": ["page_count", "format", "author", "publisher"]
    },
    "gaming-accessories": {
        "title": "Gaming Accessories",
        "subcategories": ["mechanical-keyboards", "gaming-mice", "headsets", "desk-mats"],
        "attribute_keys": ["switch_type", "dpi_sensor", "polling_rate", "dimensions"]
    }
}

class CatalogSpecValidator:
    """Utility class to validate product specification dictionaries and metadata."""
    
    @classmethod
    def validate_product_payload(cls, payload: Dict[str, Any]) -> List[str]:
        errors = []
        required_keys = ["slug", "name", "category_slug", "brand_name", "base_price", "image_url"]
        for k in required_keys:
            if k not in payload or not payload[k]:
                errors.append(f"Missing required payload key: {k}")
        
        if "base_price" in payload and payload["base_price"] <= 0:
            errors.append("Base price must be greater than zero")

        return errors

    @classmethod
    def get_category_attribute_keys(cls, category_slug: str) -> List[str]:
        return TAXONOMY_TREE.get(category_slug, {}).get("attribute_keys", [])
