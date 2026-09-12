import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.catalog.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Synchronizes all catalog products with their matching photographic image files in media/products/<slug>.jpg'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report matches without modifying database records',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')

        self.stdout.write(self.style.NOTICE(f"Scanning media directory: {media_products_dir}"))
        if not os.path.exists(media_products_dir):
            self.stderr.write(self.style.ERROR(f"Directory does not exist: {media_products_dir}"))
            return

        products = list(Product.objects.all().order_by('category__name', 'name'))
        total_products = len(products)
        self.stdout.write(self.style.NOTICE(f"Found {total_products} products in database."))

        updated_count = 0
        already_synced = 0
        missing_files = []

        for p in products:
            image_filename = f"{p.slug}.jpg"
            image_disk_path = os.path.join(media_products_dir, image_filename)
            expected_url = f"/media/products/{image_filename}"

            if not os.path.exists(image_disk_path):
                missing_files.append((p.id, p.name, p.slug))
                self.stderr.write(self.style.WARNING(f"File missing on disk for '{p.name}' ({image_filename})"))
                continue

            file_size_kb = round(os.path.getsize(image_disk_path) / 1024, 1)

            # Query existing primary image
            primary_img = p.images.filter(is_primary=True).first()
            
            if not primary_img:
                primary_img = p.images.first()

            if primary_img:
                if primary_img.image_url != expected_url or not primary_img.is_primary:
                    if not dry_run:
                        primary_img.image_url = expected_url
                        primary_img.is_primary = True
                        primary_img.display_order = 1
                        primary_img.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  [UPDATED] {p.name[:35]:35s} -> {expected_url} ({file_size_kb} KB)")
                    )
                else:
                    already_synced += 1
            else:
                if not dry_run:
                    ProductImage.objects.create(
                        product=p,
                        image_url=expected_url,
                        is_primary=True,
                        display_order=1,
                    )
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  [CREATED] {p.name[:35]:35s} -> {expected_url} ({file_size_kb} KB)")
                )

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.NOTICE("Image Synchronization Summary:"))
        self.stdout.write(f"  Total Products Processed: {total_products}")
        self.stdout.write(f"  Updated / Created:        {updated_count}")
        self.stdout.write(f"  Already Synced:           {already_synced}")
        self.stdout.write(f"  Missing Disk Files:       {len(missing_files)}")
        self.stdout.write("=" * 60 + "\n")

        if missing_files:
            self.stderr.write(self.style.ERROR(f"Alert: {len(missing_files)} products are missing image files!"))
        else:
            self.stdout.write(
                self.style.SUCCESS("All products successfully matched with verified local photographic images!")
            )
