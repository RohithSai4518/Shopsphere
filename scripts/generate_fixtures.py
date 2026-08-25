#!/usr/bin/env python3
import json
import os
import sys

# Add project root directory to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from data.catalog_expanded_dataset import EXPANDED_CATEGORIES, EXPANDED_BRANDS, RAW_PRODUCT_CATALOG

def generate_large_fixtures():
    fixtures = []

    # 1. Categories
    for cdata in EXPANDED_CATEGORIES:
        cat_id = f"cat_{cdata['slug'].replace('-', '_')}"
        fixtures.append({
            "model": "catalog.category",
            "pk": cat_id,
            "fields": {
                "parent": None,
                "name": cdata['name'],
                "slug": cdata['slug'],
                "description": cdata['description'],
                "icon_url": cdata['icon_url'],
                "is_active": True,
                "display_order": cdata['display_order'],
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    # 2. Brands
    for i, bdata in enumerate(EXPANDED_BRANDS, 1):
        fixtures.append({
            "model": "catalog.brand",
            "pk": bdata.get('id', f"brd_{i:03d}"),
            "fields": {
                "name": bdata['name'],
                "logo_url": "https://images.unsplash.com/photo-1517336714731",
                "website": bdata['website'],
                "description": bdata['description'],
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    # 3. Products, Variants, Specifications, Images, Inventory, Reviews
    for idx, pdata in enumerate(RAW_PRODUCT_CATALOG, 1):
        prd_id = f"prd_gen_{idx:04d}"
        cat_id = f"cat_{pdata['category_slug'].replace('-', '_')}"
        
        fixtures.append({
            "model": "catalog.product",
            "pk": prd_id,
            "fields": {
                "seller": "sel_001_apex",
                "category": cat_id,
                "brand": "brd_apex_01",
                "name": pdata['name'],
                "slug": pdata['slug'],
                "brand_name": pdata['brand_name'],
                "description": pdata['description'],
                "base_price": str(pdata['base_price']),
                "discount_percent": str(pdata['discount_percent']),
                "tax_rate": "8.25",
                "status": "PUBLISHED",
                "is_featured": pdata.get('is_featured', False),
                "is_bestseller": pdata.get('is_bestseller', False),
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        })

        # Variants
        for vidx, vdata in enumerate(pdata.get('variants', []), 1):
            var_id = f"var_gen_{idx:04d}_{vidx:02d}"
            fixtures.append({
                "model": "catalog.productvariant",
                "pk": var_id,
                "fields": {
                    "product": prd_id,
                    "sku": vdata['sku'],
                    "variant_name": vdata['variant_name'],
                    "price_override": str(vdata['price']),
                    "attributes_json": json.dumps(vdata.get('attrs', {})),
                    "created_at": "2026-01-01T00:00:00Z"
                }
            })

            # Inventory
            fixtures.append({
                "model": "inventory.inventory",
                "pk": f"inv_gen_{idx:04d}_{vidx:02d}",
                "fields": {
                    "variant": var_id,
                    "quantity_on_hand": 100,
                    "quantity_reserved": 2,
                    "reorder_threshold": 10,
                    "updated_at": "2026-01-01T00:00:00Z"
                }
            })

        # Primary Image
        fixtures.append({
            "model": "catalog.productimage",
            "pk": f"img_gen_{idx:04d}_1",
            "fields": {
                "product": prd_id,
                "image_url": pdata['image_url'],
                "is_primary": True,
                "display_order": 1
            }
        })

        # Specifications
        for sidx, spec in enumerate(pdata.get('specs', []), 1):
            s_key, s_val, s_grp = spec
            fixtures.append({
                "model": "catalog.productspecification",
                "pk": f"spec_gen_{idx:04d}_{sidx}",
                "fields": {
                    "product": prd_id,
                    "spec_key": s_key,
                    "spec_value": s_val,
                    "display_group": s_grp
                }
            })

        # Review
        fixtures.append({
            "model": "reviews.review",
            "pk": f"rev_gen_{idx:04d}",
            "fields": {
                "product": prd_id,
                "user": "usr_seed_merchant1",
                "rating": 5 if pdata.get('is_bestseller') else 4,
                "title": f"Excellent quality {pdata['name']}",
                "comment": f"I have been using {pdata['name']} daily. Outstanding performance and build quality.",
                "is_verified_purchase": True,
                "status": "APPROVED",
                "helpful_votes": 12,
                "unhelpful_votes": 0,
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    target_path = os.path.join(root_dir, 'fixtures', 'marketplace_catalog_expanded.json')
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, indent=2)

    print(f"Generated {len(fixtures)} database fixture objects in {target_path}.")

if __name__ == '__main__':
    generate_large_fixtures()
