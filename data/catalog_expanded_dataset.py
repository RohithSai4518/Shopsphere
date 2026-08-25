"""
Expanded Product Catalog Dataset Module for ShopSphere E-Commerce Platform.
Contains rich metadata, image specifications, technical specifications, variants, and initial reviews
for 50 realistic products across 13 major e-commerce categories.
"""

EXPANDED_CATEGORIES = [
    {
        "slug": "electronics",
        "name": "Electronics & Gadgets",
        "description": "Smart projectors, drones, power banks, VR headsets, and consumer electronics.",
        "icon_url": "laptop",
        "display_order": 1
    },
    {
        "slug": "smartphones",
        "name": "Mobiles & Smartphones",
        "description": "5G smartphones, tablets, foldable devices, and mobile technology.",
        "icon_url": "mobile",
        "display_order": 2
    },
    {
        "slug": "laptops",
        "name": "Laptops & Computers",
        "description": "High performance developer laptops, workstations, ultrabooks, and mini PCs.",
        "icon_url": "desktop",
        "display_order": 3
    },
    {
        "slug": "audio-headphones",
        "name": "Headphones & Audio",
        "description": "Active noise-cancelling headphones, wireless earbuds, studio speakers, and soundbars.",
        "icon_url": "headphones",
        "display_order": 4
    },
    {
        "slug": "smartwatches",
        "name": "Smartwatches & Wearables",
        "description": "Fitness trackers, titanium smartwatches, heart rate monitors, and GPS sports watches.",
        "icon_url": "watch",
        "display_order": 5
    },
    {
        "slug": "clothing",
        "name": "Clothing & Apparel",
        "description": "All-weather outerwear, performance athletic hoodies, executive shirts, and denim jeans.",
        "icon_url": "shirt",
        "display_order": 6
    },
    {
        "slug": "shoes",
        "name": "Shoes & Footwear",
        "description": "Trail running shoes, marathon carbon racers, genuine leather oxford shoes, and sneakers.",
        "icon_url": "footwear",
        "display_order": 7
    },
    {
        "slug": "bags-accessories",
        "name": "Bags & Accessories",
        "description": "Outdoor daypacks, leather laptop briefcases, travel duffel bags, and UV sunglasses.",
        "icon_url": "bag",
        "display_order": 8
    },
    {
        "slug": "home-kitchen",
        "name": "Home & Kitchen",
        "description": "Smart espresso coffee makers, non-stick cookware sets, air purifiers, and blenders.",
        "icon_url": "home",
        "display_order": 9
    },
    {
        "slug": "beauty",
        "name": "Beauty & Personal Care",
        "description": "Daily skin care routine kits, sonic facial brushes, luxury perfumes, and electric trimmers.",
        "icon_url": "sparkles",
        "display_order": 10
    },
    {
        "slug": "sports",
        "name": "Sports & Fitness",
        "description": "Cushioned yoga mats, adjustable dumbbell sets, stationary exercise bikes, and water bottles.",
        "icon_url": "activity",
        "display_order": 11
    },
    {
        "slug": "books",
        "name": "Books & Media",
        "description": "Culinary cookbooks, modern web development handbooks, and product design guides.",
        "icon_url": "book",
        "display_order": 12
    },
    {
        "slug": "gaming-accessories",
        "name": "Gaming Accessories",
        "description": "RGB mechanical keyboards, wireless gaming mice, 7.1 surround headsets, and XXL desk mats.",
        "icon_url": "gamepad",
        "display_order": 13
    }
]

EXPANDED_BRANDS = [
    {"id": "brd_apex_01", "name": "ApexTech", "description": "High performance workstations and developer hardware.", "website": "https://apextech.local"},
    {"id": "brd_sndw_02", "name": "SoundWave", "description": "Acoustic engineering and wireless sound technology.", "website": "https://soundwave.local"},
    {"id": "brd_nvot_03", "name": "Novata", "description": "Next-generation smartphones and mobile displays.", "website": "https://novata.local"},
    {"id": "brd_spec_04", "name": "Spectra Optics", "description": "4K visual tech, smart projectors, and camera gear.", "website": "https://spectra.local"},
    {"id": "brd_fitp_05", "name": "FitPulse", "description": "Wearable health technology and biometric sensors.", "website": "https://fitpulse.local"},
    {"id": "brd_urbt_06", "name": "UrbanTrek", "description": "Weatherproof apparel, boots, and travel gear.", "website": "https://urbantrek.local"},
    {"id": "brd_luxe_07", "name": "LuxeBeauty", "description": "Premium botanical skin care and grooming products.", "website": "https://luxebeauty.local"},
    {"id": "brd_gfor_08", "name": "GameForge", "description": "Precision gaming peripherals and esports equipment.", "website": "https://gameforge.local"},
    {"id": "brd_hchf_09", "name": "HomeChef", "description": "Smart kitchen appliances and durable cookware.", "website": "https://homechef.local"},
    {"id": "brd_ptur_10", "name": "PageTurner", "description": "Educational literature, tech handbooks, and media.", "website": "https://pageturner.local"}
]

RAW_PRODUCT_CATALOG = [
    # 1. Electronics
    {
        "slug": "quantumx-4k-smart-projector",
        "name": "QuantumX 4K Ultra HD Smart Home Cinema Projector",
        "category_slug": "electronics",
        "brand_name": "Spectra Optics",
        "description": "Experience true 4K cinematic clarity with 3000 ANSI lumens, HDR10+ support, integrated Harman Kardon speakers, and ultra-quiet cooling fan system.",
        "base_price": 499.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "QX-PROJ-STD", "variant_name": "Standard Matte Black", "price": 499.99, "attrs": {"color": "Matte Black", "lumens": "3000 ANSI"}},
            {"sku": "QX-PROJ-SLV", "variant_name": "Silver Edition", "price": 549.99, "attrs": {"color": "Silver", "lumens": "3500 ANSI"}}
        ],
        "specs": [
            ("Native Resolution", "3840 x 2160 (4K UHD)", "Display"),
            ("Brightness", "3000 ANSI Lumens", "Performance"),
            ("Projection Size", "40 to 200 inches", "Display")
        ]
    },
    {
        "slug": "aerotech-drone-pro-4k",
        "name": "AeroTech Pro 4K Dual-Camera GPS Drone",
        "category_slug": "electronics",
        "brand_name": "Spectra Optics",
        "description": "Professional foldable drone featuring a 3-axis gimbal 4K HDR camera, 45-minute flight time, omnidirectional obstacle avoidance, and 10km HD video transmission.",
        "base_price": 649.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "AT-DRONE-FLY", "variant_name": "Fly More Combo (3 Batteries)", "price": 649.99, "attrs": {"bundle": "Fly More Combo"}}
        ],
        "specs": [
            ("Camera Sensor", "1-inch CMOS 20MP", "Optics"),
            ("Flight Time", "45 Minutes per charge", "Battery"),
            ("Transmission Range", "10 Kilometers HD", "Connectivity")
        ]
    },
    {
        "slug": "hyperion-powerbank-25000mah",
        "name": "Hyperion 25,000mAh 100W Fast-Charging Power Bank",
        "category_slug": "electronics",
        "brand_name": "ApexTech",
        "description": "High-capacity portable battery pack capable of fast charging laptops, tablets, and phones simultaneously with dual USB-C Power Delivery ports.",
        "base_price": 79.99,
        "discount_percent": 5.00,
        "image_url": "https://images.unsplash.com/photo-1609592424074-1a98075bc7ea?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "HYP-PB-25K", "variant_name": "Graphite Black", "price": 79.99, "attrs": {"capacity": "25000mAh", "output": "100W Max"}}
        ],
        "specs": [
            ("Battery Capacity", "25,000mAh / 92.5Wh", "Battery"),
            ("Max Output", "100W USB-C Power Delivery", "Power")
        ]
    },
    {
        "slug": "matrix-vr-vision-pro",
        "name": "Matrix VR Vision Pro Standalone VR Headset",
        "category_slug": "electronics",
        "brand_name": "Spectra Optics",
        "description": "Next-generation standalone virtual reality headset featuring 4K per-eye resolution, spatial audio, pass-through color cameras, and ergonomic counterbalanced head strap.",
        "base_price": 599.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1622979135225-d2ba269bc1bd?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "MTX-VR-256", "variant_name": "256GB Storage", "price": 599.99, "attrs": {"storage": "256GB"}},
            {"sku": "MTX-VR-512", "variant_name": "512GB Storage", "price": 699.99, "attrs": {"storage": "512GB"}}
        ],
        "specs": [
            ("Display Resolution", "2160 x 2160 per eye (4K total)", "Display"),
            ("Refresh Rate", "120Hz Smooth Display", "Performance")
        ]
    },

    # 2. Mobiles & Smartphones
    {
        "slug": "nova-phone-z1",
        "name": "Nova Phone Z1 Flagship 5G Smartphone",
        "category_slug": "smartphones",
        "brand_name": "Novata",
        "description": "A modern 5G smartphone with a bright 6.7-inch 120Hz OLED display, triple 50MP camera array, fast wireless charging, and all-day battery life.",
        "base_price": 699.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "NOVA-Z1-128-BLK", "variant_name": "Midnight Black / 128GB", "price": 699.99, "attrs": {"color": "Midnight Black", "storage": "128GB"}},
            {"sku": "NOVA-Z1-256-SLV", "variant_name": "Frost Silver / 256GB", "price": 799.99, "attrs": {"color": "Frost Silver", "storage": "256GB"}}
        ],
        "specs": [
            ("Processor", "Octa-core 4nm Flagship Chip", "Performance"),
            ("Main Camera", "50MP Triple Lens with OIS", "Camera"),
            ("Battery", "5000mAh with 65W Fast Charge", "Power")
        ]
    },
    {
        "slug": "nova-tablet-air-11",
        "name": "Nova Tablet Air 11 Ultra",
        "category_slug": "smartphones",
        "brand_name": "Novata",
        "description": "Ultra-thin 11-inch liquid retina display tablet designed for content creators, digital drawing, and multitasking with pen stylus support.",
        "base_price": 429.99,
        "discount_percent": 12.00,
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "TAB-AIR-128", "variant_name": "128GB WiFi", "price": 429.99, "attrs": {"connectivity": "WiFi", "storage": "128GB"}}
        ],
        "specs": [
            ("Screen Size", "11.0 inch IPS Display 120Hz", "Display"),
            ("Weight", "460 grams", "Design")
        ]
    },
    {
        "slug": "vanguard-fold-pro-5g",
        "name": "Vanguard Fold Pro 5G Dual Screen Smartphone",
        "category_slug": "smartphones",
        "brand_name": "Novata",
        "description": "Revolutionary foldable OLED smartphone that seamlessly transforms from a sleek phone into an 8-inch tablet screen with zero crease hinge tech.",
        "base_price": 1199.99,
        "discount_percent": 8.00,
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "VAN-FOLD-512", "variant_name": "Phantom Black / 512GB", "price": 1199.99, "attrs": {"color": "Phantom Black", "storage": "512GB"}}
        ],
        "specs": [
            ("Unfolded Display", "8.0 inch Dynamic AMOLED 120Hz", "Display"),
            ("Hinge Design", "Armor Aluminum Dual Hinge", "Build")
        ]
    },
    {
        "slug": "titan-mobile-lite-5g",
        "name": "Titan Mobile Lite 5G Smartphone",
        "category_slug": "smartphones",
        "brand_name": "Novata",
        "description": "Essential budget-friendly 5G smartphone featuring a long-lasting 6000mAh battery, crisp FHD+ display, and clean Android interface.",
        "base_price": 299.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "TITAN-LITE-64", "variant_name": "Ocean Blue / 64GB", "price": 299.99, "attrs": {"color": "Ocean Blue", "storage": "64GB"}}
        ],
        "specs": [
            ("Battery Capacity", "6000mAh Heavy Duty", "Battery"),
            ("Network", "Dual SIM 5G Global Bands", "Connectivity")
        ]
    },

    # 3. Laptops & Computers (Existing ApexPro X15 preserved + new items)
    {
        "slug": "apexpro-x15-ultra-laptop",
        "name": "ApexPro X15 Ultra Laptop",
        "category_slug": "laptops",
        "brand_name": "ApexTech",
        "description": "The ApexPro X15 features an 8-core CPU, 32GB RAM, 1TB NVMe SSD, and 15.6-inch 4K OLED display.",
        "base_price": 1499.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "APX-X15-32GB", "variant_name": "32GB RAM / 1TB SSD Workstation", "price": 1499.99, "attrs": {"color": "Space Gray", "ram": "32GB"}}
        ],
        "specs": [
            ("Processor", "8-Core Ultra Chip 4.2GHz", "Performance"),
            ("Memory", "32GB LPDDR5X", "Performance")
        ]
    },
    {
        "slug": "apexbook-air-m2-ultrabook",
        "name": "ApexBook Air Ultra-Slim Metal Ultrabook",
        "category_slug": "laptops",
        "brand_name": "ApexTech",
        "description": "Featherlight 13.3-inch aluminum laptop featuring fanless silent design, 18-hour battery endurance, and quad speaker system.",
        "base_price": 1199.99,
        "discount_percent": 5.00,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "APX-AIR-16GB", "variant_name": "Starlight Gold / 16GB / 512GB", "price": 1199.99, "attrs": {"color": "Starlight", "ram": "16GB"}}
        ],
        "specs": [
            ("Weight", "1.24 kg (2.7 lbs)", "Design"),
            ("Battery Life", "Up to 18 hours video playback", "Battery")
        ]
    },
    {
        "slug": "titan-workstation-studio-pro",
        "name": "Titan Workstation Studio Pro Desktop PC",
        "category_slug": "laptops",
        "brand_name": "ApexTech",
        "description": "Extreme performance desktop creator workstation equipped with 16-core CPU, liquid cooling tower, 64GB DDR5 RAM, and RTX studio GPU.",
        "base_price": 2499.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "TITAN-DESK-64GB", "variant_name": "Studio Edition / 64GB RAM / 2TB NVMe", "price": 2499.99, "attrs": {"ram": "64GB", "gpu": "RTX Studio"}}
        ],
        "specs": [
            ("Processor", "16-Core 32-Thread 5.2GHz", "Performance"),
            ("Cooling", "360mm Liquid AIO Cooler", "Hardware")
        ]
    },
    {
        "slug": "novata-mini-pc-pro",
        "name": "Novata Mini PC Pro Ultra-Compact Desktop",
        "category_slug": "laptops",
        "brand_name": "Novata",
        "description": "Palm-sized desktop computer featuring triple 4K display output, dual Ethernet ports, Wi-Fi 6E, and expandability up to 64GB RAM.",
        "base_price": 449.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "MINI-PC-32GB", "variant_name": "32GB RAM / 512GB SSD", "price": 449.99, "attrs": {"size": "Compact 4x4 inch"}}
        ],
        "specs": [
            ("Dimensions", "117 x 112 x 38 mm", "Form Factor"),
            ("Display Output", "Triple 4K @ 60Hz HDMI & Type-C", "Graphics")
        ]
    },

    # 4. Headphones & Audio (Existing SoundWave Headphones preserved + new items)
    {
        "slug": "soundwave-pro-active-noise-cancelling-headphones",
        "name": "SoundWave Pro Active Noise Cancelling Headphones",
        "category_slug": "audio-headphones",
        "brand_name": "SoundWave",
        "description": "Studio-grade wireless over-ear headphones with hybrid active noise cancellation and 40-hour playtime.",
        "base_price": 249.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "SW-PRO-BLK", "variant_name": "Midnight Black", "price": 249.99, "attrs": {"color": "Midnight Black", "anc": "Active"}}
        ],
        "specs": [
            ("Battery Life", "40 Hours with ANC On", "Battery"),
            ("Driver Size", "40mm Custom Titanium Drivers", "Acoustics")
        ]
    },
    {
        "slug": "soundwave-pro-wireless-earbuds",
        "name": "SoundWave Pro ANC Wireless Earbuds",
        "category_slug": "audio-headphones",
        "brand_name": "SoundWave",
        "description": "Studio quality active noise-cancelling earbuds with 36-hour battery life and wireless charging case.",
        "base_price": 199.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "SW-ANC-BLK", "variant_name": "Matte Black", "price": 199.99, "attrs": {"color": "Matte Black"}}
        ],
        "specs": [
            ("Water Resistance", "IPX5 Sweat & Water Resistant", "Build")
        ]
    },
    {
        "slug": "studiocraft-reference-speakers",
        "name": "StudioCraft 2.0 Active Desktop Reference Monitors",
        "category_slug": "audio-headphones",
        "brand_name": "SoundWave",
        "description": "Audiophile active bookshelf speakers with optical, Bluetooth 5.0, and RCA inputs delivering crystal clear audio separation and rich punchy bass.",
        "base_price": 349.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "SC-SPK-WOOD", "variant_name": "Walnut Wood Grain", "price": 349.99, "attrs": {"finish": "Walnut Wood"}}
        ],
        "specs": [
            ("Output Power", "120W RMS Total", "Acoustics"),
            ("Inputs", "Optical, Coaxial, Bluetooth, RCA", "Connectivity")
        ]
    },
    {
        "slug": "soundpulse-waterproof-speaker",
        "name": "SoundPulse Rugged Outdoor Bluetooth Speaker",
        "category_slug": "audio-headphones",
        "brand_name": "SoundWave",
        "description": "IP67 waterproof floating portable wireless speaker with 360-degree surround sound and 24-hour continuous playback battery.",
        "base_price": 89.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "SP-SPK-RED", "variant_name": "Crimson Red", "price": 89.99, "attrs": {"color": "Crimson Red"}}
        ],
        "specs": [
            ("IP Rating", "IP67 Dustproof & Waterproof", "Protection")
        ]
    },

    # 5. Smartwatches
    {
        "slug": "fitpulse-watch-pro",
        "name": "FitPulse Watch Pro Health & Fitness Tracker",
        "category_slug": "smartwatches",
        "brand_name": "FitPulse",
        "description": "Advanced health smartwatch featuring continuous SpO2 oxygen monitoring, ECG heart tracking, sleep analysis, and built-in GPS.",
        "base_price": 179.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "FIT-PRO-BLK", "variant_name": "Black Silicone Band", "price": 179.99, "attrs": {"band": "Silicone Black"}}
        ],
        "specs": [
            ("Sensors", "ECG, SpO2, Heart Rate, GPS", "Sensors"),
            ("Water Depth", "50 Meters (5 ATM)", "Protection")
        ]
    },
    {
        "slug": "apex-chrono-smartwatch-titanium",
        "name": "Apex Chrono Titanium Luxury Smartwatch",
        "category_slug": "smartwatches",
        "brand_name": "FitPulse",
        "description": "Crafted from aerospace-grade titanium with sapphire glass screen, sapphire touch bezel, stainless mesh strap, and 14-day battery life.",
        "base_price": 299.99,
        "discount_percent": 5.00,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "APX-CHR-TIT", "variant_name": "Titanium Gray Mesh", "price": 299.99, "attrs": {"case": "Titanium Grade 5"}}
        ],
        "specs": [
            ("Glass", "Sapphire Crystal Scratch-Resistant", "Display"),
            ("Battery", "14 Days Typical Usage", "Power")
        ]
    },
    {
        "slug": "activegear-gps-sports-watch",
        "name": "ActiveGear Tough Outdoor GPS Sports Watch",
        "category_slug": "smartwatches",
        "brand_name": "FitPulse",
        "description": "Military standard rugged sports watch with topographic maps, dual-frequency multi-GNSS tracking, barometer, and solar charging display lens.",
        "base_price": 149.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "ACT-GPS-MIL", "variant_name": "Tactical Olive Green", "price": 149.99, "attrs": {"color": "Tactical Olive"}}
        ],
        "specs": [
            ("GPS Standard", "Dual Frequency L1+L5 GNSS", "Navigation")
        ]
    },

    # 6. Clothing
    {
        "slug": "urbantrek-waterproof-jacket",
        "name": "UrbanTrek All-Weather Breathable Waterproof Jacket",
        "category_slug": "clothing",
        "brand_name": "UrbanTrek",
        "description": "3-layer seam-sealed waterproof rain jacket with adjustable hood, underarm ventilation zips, and packable pocket design.",
        "base_price": 129.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "UT-JCK-M-BLK", "variant_name": "Black / Medium", "price": 129.99, "attrs": {"size": "Medium", "color": "Black"}},
            {"sku": "UT-JCK-L-BLK", "variant_name": "Black / Large", "price": 129.99, "attrs": {"size": "Large", "color": "Black"}}
        ],
        "specs": [
            ("Waterproof Rating", "20,000mm Hydrostatic Head", "Fabric"),
            ("Material", "100% Recycled Nylon Shell", "Material")
        ]
    },
    {
        "slug": "aerofit-performance-hoodie",
        "name": "AeroFit Thermal Performance Athletic Hoodie",
        "category_slug": "clothing",
        "brand_name": "UrbanTrek",
        "description": "Moisture-wicking 4-way stretch fleece hoodie with thumbhole cuffs, zip phone pocket, and athletic tapered fit.",
        "base_price": 59.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "AERO-HD-GRY-L", "variant_name": "Heather Gray / Large", "price": 59.99, "attrs": {"color": "Heather Gray", "size": "Large"}}
        ],
        "specs": [
            ("Fabric Weight", "280 GSM Stretch Fleece", "Fabric")
        ]
    },
    {
        "slug": "luxesilk-executive-shirt",
        "name": "LuxeSilk Wrinkle-Free Executive Cotton Shirt",
        "category_slug": "clothing",
        "brand_name": "UrbanTrek",
        "description": "100% Supima long-staple cotton dress shirt featuring stain-resistant finish, reinforced collar stays, and tailored cut.",
        "base_price": 79.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "LUXE-SHIRT-WHT-16", "variant_name": "Crisp White / 16-34", "price": 79.99, "attrs": {"color": "White", "size": "16-34"}}
        ],
        "specs": [
            ("Weave", "Pinpoint Oxford 100% Cotton", "Fabric")
        ]
    },
    {
        "slug": "denimcraft-vintage-jeans",
        "name": "DenimCraft Vintage Slim Fit Comfort Denim Jeans",
        "category_slug": "clothing",
        "brand_name": "UrbanTrek",
        "description": "Classic 5-pocket selvedge denim jeans woven with 2% elastane flex for full mobility and effortless everyday style.",
        "base_price": 69.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "DENIM-32-32", "variant_name": "Indigo Wash / 32x32", "price": 69.99, "attrs": {"size": "32x32", "color": "Indigo Wash"}}
        ],
        "specs": [
            ("Denim Weight", "12.5 oz Selvedge Denim", "Material")
        ]
    },

    # 7. Shoes
    {
        "slug": "northstar-running-shoes",
        "name": "NorthStar Trail Running Shoes",
        "category_slug": "shoes",
        "brand_name": "UrbanTrek",
        "description": "Cushioned running shoes with a breathable upper, responsive foam midsole, and grippy multi-surface outsole for trail endurance.",
        "base_price": 89.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "NORTH-SHOE-10", "variant_name": "Electric Blue / US 10", "price": 89.99, "attrs": {"size": "10", "color": "Electric Blue"}},
            {"sku": "NORTH-SHOE-11", "variant_name": "Electric Blue / US 11", "price": 89.99, "attrs": {"size": "11", "color": "Electric Blue"}}
        ],
        "specs": [
            ("Midsole Foam", "Dual-Density EVA Energy Return", "Cushioning"),
            ("Drop", "8mm Heel-to-Toe Drop", "Geometry")
        ]
    },
    {
        "slug": "apex-carbon-marathon-shoes",
        "name": "Apex Carbon Plate Marathon Racing Shoes",
        "category_slug": "shoes",
        "brand_name": "UrbanTrek",
        "description": "Ultra-lightweight competitive marathon shoe engineered with full-length curved carbon fiber plate and nitrogen-infused superfoam.",
        "base_price": 159.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "APX-CARB-105", "variant_name": "Neon Yellow / US 10.5", "price": 159.99, "attrs": {"color": "Neon Yellow", "size": "10.5"}}
        ],
        "specs": [
            ("Weight", "185 grams per shoe", "Specs")
        ]
    },
    {
        "slug": "urbanstep-leather-oxfords",
        "name": "UrbanStep Handcrafted Genuine Leather Oxford Shoes",
        "category_slug": "shoes",
        "brand_name": "UrbanTrek",
        "description": "Formal full-grain Italian leather dress shoes with Goodyear welt construction and cushioned memory foam insole.",
        "base_price": 119.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "OXFORD-BRN-10", "variant_name": "Cognac Brown / US 10", "price": 119.99, "attrs": {"color": "Cognac Brown", "size": "10"}}
        ],
        "specs": [
            ("Construction", "Goodyear Welted Re-craftable Sole", "Build")
        ]
    },

    # 8. Bags & Accessories
    {
        "slug": "trailblazer-outdoor-daypack",
        "name": "TrailBlazer Outdoor Daypack 30L",
        "category_slug": "bags-accessories",
        "brand_name": "UrbanTrek",
        "description": "Weather-resistant 30L backpack featuring padded 16-inch laptop compartment, hydration bladder sleeve, and ergonomic air-mesh back panel.",
        "base_price": 74.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "TB-PACK-GRN", "variant_name": "Forest Green 30L", "price": 74.99, "attrs": {"capacity": "30L", "color": "Forest Green"}}
        ],
        "specs": [
            ("Volume", "30 Liters", "Capacity"),
            ("Material", "600D Ripstop Cordura Nylon", "Durability")
        ]
    },
    {
        "slug": "executive-leather-briefcase",
        "name": "Executive Full-Grain Leather Briefcase & Laptop Bag",
        "category_slug": "bags-accessories",
        "brand_name": "UrbanTrek",
        "description": "Handcrafted leather Messenger messenger bag with padded tablet section, brass hardware, and detachable padded shoulder strap.",
        "base_price": 149.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "EXEC-BAG-TAN", "variant_name": "Tan Saddle Leather", "price": 149.99, "attrs": {"color": "Tan Saddle"}}
        ],
        "specs": [
            ("Laptop Compatibility", "Fits up to 15.6-inch Laptops", "Fit")
        ]
    },
    {
        "slug": "voyager-anti-theft-travel-duffel",
        "name": "Voyager Anti-Theft Water-Resistant Travel Duffel Bag",
        "category_slug": "bags-accessories",
        "brand_name": "UrbanTrek",
        "description": "50L convertible carry-on duffel bag with isolated shoe pocket, TSA-approved combination lock zippers, and hideaway backpack straps.",
        "base_price": 99.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "VOY-DUFFEL-BLK", "variant_name": "Stealth Black 50L", "price": 99.99, "attrs": {"capacity": "50L"}}
        ],
        "specs": [
            ("Carry-On Size", "22 x 14 x 9 inches (FAA Compliant)", "Dimensions")
        ]
    },
    {
        "slug": "aeroshield-polarized-sunglasses",
        "name": "AeroShield Polarized UV400 Sunglasses",
        "category_slug": "bags-accessories",
        "brand_name": "UrbanTrek",
        "description": "Classic aviator style sunglasses with TAC polarized lenses, lightweight titanium frame, and anti-reflective coating.",
        "base_price": 49.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "AERO-SUN-BLK", "variant_name": "Gunmetal / Dark Gray Lens", "price": 49.99, "attrs": {"frame": "Gunmetal"}}
        ],
        "specs": [
            ("UV Protection", "100% UV400 Protection", "Optical")
        ]
    },

    # 9. Home & Kitchen
    {
        "slug": "homebrew-smart-coffee-maker",
        "name": "HomeBrew Smart Espresso Coffee Maker",
        "category_slug": "home-kitchen",
        "brand_name": "HomeChef",
        "description": "Programmable espresso machine with integrated conical burr grinder, 15-bar Italian pump pressure, and automatic milk frother.",
        "base_price": 129.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "HOMEBREW-ESP-SS", "variant_name": "Brushed Stainless Steel", "price": 129.99, "attrs": {"finish": "Stainless Steel"}}
        ],
        "specs": [
            ("Pump Pressure", "15 Bar High Pressure Pump", "Performance"),
            ("Water Reservoir", "2.0 Liters Removable Tank", "Capacity")
        ]
    },
    {
        "slug": "chefline-cookware-set",
        "name": "ChefLine 10-Piece Hard-Anodized Cookware Set",
        "category_slug": "home-kitchen",
        "brand_name": "HomeChef",
        "description": "Heavy-gauge hard-anodized non-stick cookware set including saucepans, stockpot, skillet pans, and tempered glass lids.",
        "base_price": 159.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "CHEF-COOK-10P", "variant_name": "10-Piece Complete Set", "price": 159.99, "attrs": {"pieces": "10"}}
        ],
        "specs": [
            ("Oven Safe Temperature", "Up to 500°F (260°C)", "Durability")
        ]
    },
    {
        "slug": "airflow-smart-hepa-purifier",
        "name": "AirFlow Pro Smart True HEPA Air Purifier",
        "category_slug": "home-kitchen",
        "brand_name": "HomeChef",
        "description": "Quiet room air purifier featuring H13 True HEPA filter, real-time AQI air quality display sensor, and smartphone app control.",
        "base_price": 189.99,
        "discount_percent": 5.00,
        "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "AIR-PUR-PRO", "variant_name": "White Tower / 500 sq. ft.", "price": 189.99, "attrs": {"coverage": "500 sq ft"}}
        ],
        "specs": [
            ("Filtration Efficiency", "99.97% of particles down to 0.3 microns", "Filtration")
        ]
    },
    {
        "slug": "culinaryblender-1200w-blender",
        "name": "CulinaryBlender 1200W Professional Countertop Blender",
        "category_slug": "home-kitchen",
        "brand_name": "HomeChef",
        "description": "Commercial-grade 1200W blender with 6-leaf stainless steel crushing blades, 64 oz Tritan pitcher, and pre-programmed smoothie presets.",
        "base_price": 99.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "BLEND-1200W", "variant_name": "Black / 64oz Pitcher", "price": 99.99, "attrs": {"power": "1200W"}}
        ],
        "specs": [
            ("Motor Output", "1200 Watts Peak Power", "Motor")
        ]
    },

    # 10. Beauty & Personal Care
    {
        "slug": "luma-skin-care-kit",
        "name": "Luma Daily Hydrating Skin Care Routine Kit",
        "category_slug": "beauty",
        "brand_name": "LuxeBeauty",
        "description": "Complete 4-piece skincare essential bundle including gentle foaming cleanser, vitamin C serum, hyaluronic acid gel, and mineral SPF 30.",
        "base_price": 54.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "LUMA-SKIN-KIT", "variant_name": "Complete 4-Piece Kit", "price": 54.99, "attrs": {"skin_type": "All Skin Types"}}
        ],
        "specs": [
            ("Key Ingredients", "Vitamin C, Hyaluronic Acid, Niacinamide", "Ingredients")
        ]
    },
    {
        "slug": "glowpro-sonic-facial-cleansing-brush",
        "name": "GlowPro Waterproof Sonic Facial Cleansing Brush",
        "category_slug": "beauty",
        "brand_name": "LuxeBeauty",
        "description": "Ultra-hygienic silicone sonic cleansing device with 8 adjustable pulsation intensities and thermal massage warming mode.",
        "base_price": 39.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "GLOW-BRUSH-PNK", "variant_name": "Rose Pink Silicone", "price": 39.99, "attrs": {"color": "Rose Pink"}}
        ],
        "specs": [
            ("Pulsations", "8000 Sonic Pulsations per minute", "Technology")
        ]
    },
    {
        "slug": "velvetaroma-perfume-set",
        "name": "VelvetAroma Deluxe Fragrance Spray Gift Set",
        "category_slug": "beauty",
        "brand_name": "LuxeBeauty",
        "description": "Elegant collection of 3 artisanal long-lasting eau de parfum fragrances featuring notes of amber vanilla, bergamot cedar, and jasmine bloom.",
        "base_price": 89.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "VELVET-PERF-3PK", "variant_name": "Trio Discovery Set (3x50ml)", "price": 89.99, "attrs": {"volume": "3x 50ml"}}
        ],
        "specs": [
            ("Concentration", "Eau de Parfum (20% Essential Oils)", "Fragrance")
        ]
    },
    {
        "slug": "progroom-hair-beard-trimmer",
        "name": "ProGroom Cordless Waterproof Hair & Beard Trimmer",
        "category_slug": "beauty",
        "brand_name": "LuxeBeauty",
        "description": "Self-sharpening titanium blade grooming kit with 10 precision length combs, LED battery indicator, and 120-minute lithium battery.",
        "base_price": 45.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "PRO-TRIM-SLV", "variant_name": "Matte Silver / 10 Combs", "price": 45.99, "attrs": {"blades": "Self-Sharpening Titanium"}}
        ],
        "specs": [
            ("Run Time", "120 Minutes on 1-hour fast charge", "Battery")
        ]
    },

    # 11. Sports & Fitness
    {
        "slug": "peak-performance-yoga-mat",
        "name": "Peak Performance Non-Slip Cushion Yoga Mat",
        "category_slug": "sports",
        "brand_name": "FitPulse",
        "description": "6mm extra-thick eco-friendly TPE exercise mat featuring dual texture non-slip alignment lines and carrying strap included.",
        "base_price": 39.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "PEAK-YOGA-PUR", "variant_name": "Deep Purple / 6mm", "price": 39.99, "attrs": {"thickness": "6mm", "color": "Deep Purple"}}
        ],
        "specs": [
            ("Thickness", "6mm High Density Cushion", "Dimensions"),
            ("Eco Certification", "100% Non-Toxic TPE (PVC Free)", "Material")
        ]
    },
    {
        "slug": "flexpower-adjustable-dumbbell-set",
        "name": "FlexPower 52.5 lb Adjustable Quick-Select Dumbbell",
        "category_slug": "sports",
        "brand_name": "FitPulse",
        "description": "Compact single dumbbell that adjusts instantly from 5 to 52.5 lbs in 2.5 lb increments with a simple turn of the dial dial system.",
        "base_price": 199.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "FLEX-DUMB-52", "variant_name": "Single 52.5 lb Unit", "price": 199.99, "attrs": {"weight": "5-52.5 lbs"}}
        ],
        "specs": [
            ("Weight Range", "5 to 52.5 lbs (15 weight settings)", "Weight")
        ]
    },
    {
        "slug": "cardioride-smart-exercise-bike",
        "name": "CardioRide Smart Indoor Cycling Bike",
        "category_slug": "sports",
        "brand_name": "FitPulse",
        "description": "Whisper-quiet magnetic resistance studio cycle bike with Bluetooth CADENCE telemetry, tablet holder mount, and heavy 35 lb flywheel.",
        "base_price": 499.99,
        "discount_percent": 5.00,
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "CARDIO-BIKE-PRO", "variant_name": "Studio Black / Magnetic", "price": 499.99, "attrs": {"flywheel": "35 lbs"}}
        ],
        "specs": [
            ("Resistance System", "Smooth Silent Magnetic Resistance", "Drive")
        ]
    },
    {
        "slug": "hydraflow-insulated-water-bottle",
        "name": "HydraFlow 32 oz Vacuum Insulated Stainless Steel Bottle",
        "category_slug": "sports",
        "brand_name": "FitPulse",
        "description": "Double-wall vacuum insulated stainless steel water bottle keeping drinks cold for 24 hours or hot for 12 hours with straw lid.",
        "base_price": 24.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "HYDRA-32-BLK", "variant_name": "Matte Black 32 oz", "price": 24.99, "attrs": {"volume": "32 oz"}}
        ],
        "specs": [
            ("Insulation", "TempShield Double Wall Vacuum", "Thermal")
        ]
    },

    # 12. Books
    {
        "slug": "atlas-weeknight-cookbook",
        "name": "Atlas Weeknight Culinary Cookbook",
        "category_slug": "books",
        "brand_name": "PageTurner",
        "description": "Over 150 practical, wholesome recipes designed for 30-minute home dinners with step-by-step full color photography guides.",
        "base_price": 24.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "BOOK-ATLAS-HC", "variant_name": "Hardcover Edition", "price": 24.99, "attrs": {"format": "Hardcover"}}
        ],
        "specs": [
            ("Page Count", "320 Pages Full Color", "Publisher")
        ]
    },
    {
        "slug": "modern-web-dev-handbook",
        "name": "Modern Web Development & Full-Stack Architecture",
        "category_slug": "books",
        "brand_name": "PageTurner",
        "description": "Comprehensive engineering handbook covering modern frontend frameworks, REST/GraphQL APIs, database scaling, and cloud deployment.",
        "base_price": 39.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": False,
        "variants": [
            {"sku": "BOOK-WEBDEV-PB", "variant_name": "Paperback Edition", "price": 39.99, "attrs": {"format": "Paperback"}}
        ],
        "specs": [
            ("Page Count", "540 Pages Technical Reference", "Publisher")
        ]
    },
    {
        "slug": "art-of-product-design",
        "name": "The Art of Product Design & Digital User Experience",
        "category_slug": "books",
        "brand_name": "PageTurner",
        "description": "An inspiring visual guide to UX design systems, human interface principles, prototyping, and user psychology.",
        "base_price": 29.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "BOOK-DESIGN-HC", "variant_name": "Collector Hardcover", "price": 29.99, "attrs": {"format": "Hardcover"}}
        ],
        "specs": [
            ("Page Count", "280 Pages Premium Glossy", "Publisher")
        ]
    },

    # 13. Gaming Accessories
    {
        "slug": "gameforge-rgb-mechanical-keyboard",
        "name": "GameForge RGB Hot-Swappable Mechanical Gaming Keyboard",
        "category_slug": "gaming-accessories",
        "brand_name": "GameForge",
        "description": "Compact 75% mechanical keyboard featuring hot-swappable tactile switches, per-key RGB backlighting, sound-dampening foam, and braided Type-C cable.",
        "base_price": 119.99,
        "discount_percent": 15.00,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
        "is_featured": True,
        "is_bestseller": True,
        "variants": [
            {"sku": "GF-KB-RED", "variant_name": "Red Linear Switches", "price": 119.99, "attrs": {"switch": "Red Linear"}},
            {"sku": "GF-KB-BRN", "variant_name": "Brown Tactile Switches", "price": 119.99, "attrs": {"switch": "Brown Tactile"}}
        ],
        "specs": [
            ("Polling Rate", "1000Hz (1ms response)", "Performance"),
            ("Keycap Material", "Double-Shot PBT Keycaps", "Build")
        ]
    },
    {
        "slug": "gameforge-ultralight-wireless-mouse",
        "name": "GameForge UltraLight 49g Wireless Gaming Mouse",
        "category_slug": "gaming-accessories",
        "brand_name": "GameForge",
        "description": "Ergonomic 49-gram esports gaming mouse equipped with 26,000 DPI optical sensor, optical microswitches, and low-latency 2.4GHz wireless tech.",
        "base_price": 69.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": True,
        "variants": [
            {"sku": "GF-MSE-BLK", "variant_name": "Matte Black 49g", "price": 69.99, "attrs": {"weight": "49 grams"}}
        ],
        "specs": [
            ("Sensor", "PAW3395 26,000 DPI Optical", "Sensor"),
            ("Battery Life", "Up to 80 hours gaming", "Battery")
        ]
    },
    {
        "slug": "gameforge-71-surround-headset",
        "name": "GameForge 7.1 Surround Sound Gaming Headset",
        "category_slug": "gaming-accessories",
        "brand_name": "GameForge",
        "description": "Immersive gaming headset featuring 53mm neodymium drivers, detachable noise-cancelling microphone, and plush memory foam ear cushions.",
        "base_price": 89.99,
        "discount_percent": 10.00,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "GF-HS-71", "variant_name": "Midnight Black / Red Trim", "price": 89.99, "attrs": {"audio": "7.1 Virtual Surround"}}
        ],
        "specs": [
            ("Drivers", "53mm Neodymium Magnet Drivers", "Acoustics")
        ]
    },
    {
        "slug": "titandesk-xxl-gaming-mousepad",
        "name": "TitanDesk XXL Stitch-Edged Water-Resistant Mousepad",
        "category_slug": "gaming-accessories",
        "brand_name": "GameForge",
        "description": "Extra-large 900x400mm desk mat featuring micro-woven cloth surface, anti-slip rubber base, and reinforced anti-fray stitched borders.",
        "base_price": 29.99,
        "discount_percent": 0.00,
        "image_url": "https://images.unsplash.com/photo-1616440342855-49e0c5f2b842?auto=format&fit=crop&w=800&q=80",
        "is_featured": False,
        "is_bestseller": False,
        "variants": [
            {"sku": "TD-PAD-XXL", "variant_name": "900x400mm Topo Black", "price": 29.99, "attrs": {"size": "900x400mm"}}
        ],
        "specs": [
            ("Dimensions", "900mm x 400mm x 4mm", "Dimensions")
        ]
    }
]
