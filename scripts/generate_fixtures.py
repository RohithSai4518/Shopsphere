#!/usr/bin/env python3
import json
import os
import random

def generate_large_fixtures():
    fixtures = []

    categories = [
        ("cat_gen_laptops", "Workstation Laptops", "laptops", "Laptops and Notebooks"),
        ("cat_gen_smartphones", "Flagship Smartphones", "smartphones", "Mobile phones and tablets"),
        ("cat_gen_audio", "Studio Audio", "audio", "Headphones, microphones, and soundbars"),
        ("cat_gen_monitors", "UltraWide Displays", "monitors", "4K and 8K desktop displays"),
        ("cat_gen_components", "PC Hardware Components", "components", "CPUs, GPUs, and motherboards"),
        ("cat_gen_peripherals", "Gaming Peripherals", "peripherals", "Mechanical keyboards and mice"),
        ("cat_gen_networking", "Enterprise Networking", "networking", "Routers, switches, and access points"),
        ("cat_gen_storage", "NVMe & NAS Storage", "storage", "SSDs, hard drives, and network storage"),
        ("cat_gen_smarthome", "Smart Home Tech", "smarthome", "IoT sensors, cameras, and hubs"),
        ("cat_gen_accessories", "Tech Accessories", "accessories", "Cables, adapters, and power banks")
    ]

    for cat_id, name, slug, desc in categories:
        fixtures.append({
            "model": "catalog.category",
            "pk": cat_id,
            "fields": {
                "parent": None,
                "name": name,
                "slug": slug,
                "description": desc,
                "icon_url": slug,
                "is_active": True,
                "display_order": random.randint(1, 10),
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    brands = ["ApexTech", "SoundWave", "Novata", "Hyperion", "QuantumX", "Vanguard", "Titan", "Spectra", "AeroTech", "Matrix"]
    for i, bname in enumerate(brands, 1):
        fixtures.append({
            "model": "catalog.brand",
            "pk": f"brd_gen_{i:03d}",
            "fields": {
                "name": f"{bname} Enterprise Systems",
                "logo_url": "https://images.unsplash.com/photo-1517336714731",
                "website": f"https://{bname.lower()}.local",
                "description": f"Manufacturer of {bname} electronics.",
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    adjectives = ["Pro", "Ultra", "Max", "Prime", "Elite", "Apex", "Studio", "Enterprise", "Extreme", "Vanguard"]
    nouns = ["Station", "Book", "Display", "Hub", "Pad", "Core", "Link", "Tower", "Pulse", "Sonic"]

    product_count = 350
    for p in range(1, product_count + 1):
        brand = random.choice(brands)
        pname = f"{brand} {random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 999)}"
        pslug = f"{pname.lower().replace(' ', '-')}-{p}"
        cat = random.choice(categories)[0]
        price = round(random.uniform(49.99, 2499.99), 2)
        discount = random.choice([0.00, 5.00, 10.00, 15.00, 20.00])

        prd_id = f"prd_gen_{p:04d}"
        fixtures.append({
            "model": "catalog.product",
            "pk": prd_id,
            "fields": {
                "seller": "sel_001_apex",
                "category": cat,
                "brand": f"brd_gen_{random.randint(1, len(brands)):03d}",
                "name": pname,
                "slug": pslug,
                "brand_name": brand,
                "description": f"{pname} delivers enterprise performance, low latency processing, and ultra-durable build quality.",
                "base_price": str(price),
                "discount_percent": str(discount),
                "tax_rate": "8.25",
                "status": "PUBLISHED",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        })

        # Variant
        var_id = f"var_gen_{p:04d}_01"
        fixtures.append({
            "model": "catalog.productvariant",
            "pk": var_id,
            "fields": {
                "product": prd_id,
                "sku": f"SKU-{brand[:3].upper()}-{p:04d}-V1",
                "variant_name": "Standard Edition",
                "price_override": str(price),
                "attributes_json": "{\"edition\": \"Standard\"}",
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

        # Specifications
        fixtures.append({
            "model": "catalog.productspecification",
            "pk": f"spec_gen_{p:04d}_1",
            "fields": {
                "product": prd_id,
                "spec_key": "Warranty Coverage",
                "spec_value": "3-Year Commercial Warranty",
                "display_group": "General"
            }
        })
        fixtures.append({
            "model": "catalog.productspecification",
            "pk": f"spec_gen_{p:04d}_2",
            "fields": {
                "product": prd_id,
                "spec_key": "Input Voltage",
                "spec_value": "100-240V AC 50/60Hz",
                "display_group": "Power"
            }
        })

        # Image
        fixtures.append({
            "model": "catalog.productimage",
            "pk": f"img_gen_{p:04d}_1",
            "fields": {
                "product": prd_id,
                "image_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80",
                "is_primary": True,
                "display_order": 1
            }
        })

        # Inventory
        fixtures.append({
            "model": "inventory.inventory",
            "pk": f"inv_gen_{p:04d}",
            "fields": {
                "variant": var_id,
                "quantity_on_hand": random.randint(20, 200),
                "quantity_reserved": random.randint(0, 5),
                "reorder_threshold": 10,
                "updated_at": "2026-01-01T00:00:00Z"
            }
        })

        # Review
        fixtures.append({
            "model": "reviews.review",
            "pk": f"rev_gen_{p:04d}",
            "fields": {
                "product": prd_id,
                "user": "usr_seed_merchant1",
                "rating": random.choice([4, 5]),
                "title": f"Excellent quality {pname}",
                "comment": f"I have been using {pname} daily. Performance and build quality exceed expectation.",
                "is_verified_purchase": True,
                "status": "APPROVED",
                "helpful_votes": random.randint(1, 20),
                "unhelpful_votes": 0,
                "created_at": "2026-01-01T00:00:00Z"
            }
        })

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(root_dir, 'fixtures', 'marketplace_catalog_expanded.json')
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, indent=2)

    print(f"Generated {len(fixtures)} database fixture objects in {target_path}.")

if __name__ == '__main__':
    generate_large_fixtures()
