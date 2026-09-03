from django.db import models
from django.utils.text import slugify
from decimal import Decimal
import uuid
from apps.sellers.models import Seller
from apps.accounts.models import User

def generate_cat_id(): return f"cat_{uuid.uuid4().hex[:12]}"
def generate_brd_id(): return f"brd_{uuid.uuid4().hex[:12]}"
def generate_prd_id(): return f"prd_{uuid.uuid4().hex[:12]}"
def generate_var_id(): return f"var_{uuid.uuid4().hex[:12]}"
def generate_spec_id(): return f"spec_{uuid.uuid4().hex[:12]}"
def generate_img_id(): return f"img_{uuid.uuid4().hex[:12]}"
def generate_bdl_id(): return f"bdl_{uuid.uuid4().hex[:12]}"
def generate_tag_id(): return f"tag_{uuid.uuid4().hex[:12]}"
def generate_qna_id(): return f"qna_{uuid.uuid4().hex[:12]}"
def generate_ans_id(): return f"ans_{uuid.uuid4().hex[:12]}"
def generate_rel_id(): return f"rel_{uuid.uuid4().hex[:12]}"
def generate_mod_id(): return f"mod_{uuid.uuid4().hex[:12]}"

class Category(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_cat_id)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_brd_id)
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_tag_id)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_prd_id)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    brand_name = models.CharField(max_length=100, default='ApexTech')
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('8.25'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PUBLISHED')
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        base = Decimal(str(self.base_price))
        disc = Decimal(str(self.discount_percent))
        discount_amount = (base * disc) / Decimal('100.00')
        return round(base - discount_amount, 2)

    @property
    def primary_image(self):
        if hasattr(self, '_prefetched_objects_cache') and 'images' in self._prefetched_objects_cache:
            for img in self._prefetched_objects_cache['images']:
                if img.is_primary:
                    return img.image_url
            if self._prefetched_objects_cache['images']:
                return self._prefetched_objects_cache['images'][0].image_url
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img.image_url if img else 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80'

    @property
    def first_variant(self):
        if hasattr(self, '_prefetched_objects_cache') and 'variants' in self._prefetched_objects_cache:
            return self._prefetched_objects_cache['variants'][0] if self._prefetched_objects_cache['variants'] else None
        return self.variants.first()

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_var_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    variant_name = models.CharField(max_length=100)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    attributes_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name} ({self.sku})"


class ProductSpecification(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_spec_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    spec_key = models.CharField(max_length=100)
    spec_value = models.CharField(max_length=255)
    display_group = models.CharField(max_length=100, default='General')

    def __str__(self):
        return f"{self.spec_key}: {self.spec_value}"


class ProductImage(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_img_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField()
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductBundle(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_bdl_id)
    name = models.CharField(max_length=200)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BundleItem(models.Model):
    bundle = models.ForeignKey(ProductBundle, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bundles')

    class Meta:
        unique_together = ('bundle', 'product')


class ProductRelationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ('BOUGHT_TOGETHER', 'Frequently Bought Together'),
        ('RELATED', 'Related Product'),
        ('SIMILAR', 'Similar Product'),
        ('UPSELL', 'Upgrade Upsell'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_rel_id)
    source_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='source_relationships')
    target_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='target_relationships')
    relationship_type = models.CharField(max_length=30, choices=RELATIONSHIP_CHOICES, default='RELATED')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.85'))

    class Meta:
        unique_together = ('source_product', 'target_product', 'relationship_type')


class ProductQuestion(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_qna_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_questions')
    question_text = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q on {self.product.name}: {self.question_text[:50]}"


class ProductAnswer(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_ans_id)
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_answers')
    answer_text = models.TextField()
    is_seller_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductModerationLog(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_mod_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='moderation_logs')
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_moderations')
    status_from = models.CharField(max_length=30)
    status_to = models.CharField(max_length=30)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
