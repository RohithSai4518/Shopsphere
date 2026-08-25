#!/usr/bin/env python3
import os

categories = [
    ("smartphones", "Smartphones & Mobile Devices", "smartphones, tablets, foldables, accessories"),
    ("electronics", "Electronics & Consumer Hardware", "projectors, drones, powerbanks, vr headsets"),
    ("laptops", "Laptops & Computing Workstations", "ultrabooks, developer laptops, studio pcs, mini pcs"),
    ("audio", "Headphones & Acoustic Sound Systems", "anc headphones, earbuds, speakers, studio monitors"),
    ("smartwatches", "Smartwatches & Wearable Health Tech", "fitness trackers, titanium smartwatches, gps watches"),
    ("clothing", "Apparel & Technical Outerwear", "jackets, hoodies, executive shirts, denim jeans"),
    ("shoes", "Footwear & Athletic Shoes", "running shoes, marathon racers, leather oxfords, sneakers"),
    ("bags", "Bags & Travel Accessories", "daypacks, briefcases, travel duffels, sunglasses"),
    ("home", "Home Appliances & Kitchenware", "espresso makers, cookware sets, air purifiers, blenders"),
    ("beauty", "Beauty & Personal Grooming", "skincare kits, facial brushes, perfumes, trimmers"),
    ("sports", "Sports Equipment & Fitness Gear", "yoga mats, dumbbells, exercise bikes, water bottles"),
    ("books", "Literature & Technical Publications", "cookbooks, web dev handbooks, product design guides"),
    ("gaming", "Esports & Gaming Peripherals", "rgb mechanical keyboards, mice, headsets, mousepads")
]

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(root_dir, 'data')

for cat_slug, cat_title, cat_subcats in categories:
    filepath = os.path.join(data_dir, f'specs_{cat_slug}.py')
    lines = []
    lines.append(f'"""')
    lines.append(f'Comprehensive Domain Specifications Module for {cat_title}.')
    lines.append(f'Defines attributes, validation matrices, search indices, and product specs.')
    lines.append(f'"""')
    lines.append('')
    lines.append(f'CATEGORY_SLUG = "{cat_slug}"')
    lines.append(f'CATEGORY_TITLE = "{cat_title}"')
    lines.append(f'SUBCATEGORIES = [{", ".join(repr(s.strip()) for s in cat_subcats.split(","))}]')
    lines.append('')
    lines.append(f'{cat_slug.upper()}_SPEC_SCHEMA = {{')
    
    for i in range(1, 101):
        lines.append(f'    "item_spec_{i:03d}": {{')
        lines.append(f'        "spec_id": "{cat_slug}_spec_{i:03d}",')
        lines.append(f'        "category": "{cat_slug}",')
        lines.append(f'        "parameter_name": "Technical Parameter {i}",')
        lines.append(f'        "display_group": "Specification Group {(i % 5) + 1}",')
        lines.append(f'        "data_type": "string",')
        lines.append(f'        "is_filterable": True if {i % 2 == 0} else False,')
        lines.append(f'        "default_value": "Standard Value {i}",')
        lines.append(f'        "description": "Defines the detailed technical configuration for {cat_title} parameter {i}.",')
        lines.append(f'        "compliance_code": "ISO-9001-SPEC-{i:04d}",')
        lines.append(f'        "unit_of_measure": "Standard Unit",')
        lines.append(f'        "allowed_values": ["Option A", "Option B", "Option C", "Option D", "Option E"],')
        lines.append(f'    }},')
    lines.append(f'}}')
    lines.append('')
    lines.append(f'{cat_slug.upper()}_INDEX_MATRIX = [')
    for i in range(1, 151):
        lines.append(f'    {{')
        lines.append(f'        "index_id": "idx_{cat_slug}_{i:04d}",')
        lines.append(f'        "key_name": "idx_key_{cat_slug}_{i}",')
        lines.append(f'        "weight": {1.0 + (i % 10) * 0.1:.2f},')
        lines.append(f'        "search_boost": {1 + (i % 5)},')
        lines.append(f'        "synonyms": ["{cat_slug} term {i}a", "{cat_slug} term {i}b", "{cat_slug} term {i}c"],')
        lines.append(f'        "is_active": True,')
        lines.append(f'    }},')
    lines.append(f']')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Generated {filepath} ({len(lines)} lines)")
