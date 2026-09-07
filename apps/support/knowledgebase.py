import uuid
from django.db import models
from django.utils.text import slugify

def generate_faqcat_id(): return f"faqcat_{uuid.uuid4().hex[:10]}"
def generate_faqart_id(): return f"faqart_{uuid.uuid4().hex[:10]}"

class FAQCategory(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_faqcat_id)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.CharField(max_length=255, blank=True)
    icon_name = models.CharField(max_length=50, default='help-circle')
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'FAQ Categories'
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class FAQArticle(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_faqart_id)
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='articles')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    helpful_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    keywords = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-helpful_count', '-created_at']

    def __str__(self):
        return f"{self.category.title}: {self.question}"


class KnowledgeBaseService:
    """
    Search and curation engine for customer Help Center articles and FAQs.
    """

    @classmethod
    def get_all_categories(cls):
        cls.ensure_seeded_faqs()
        return FAQCategory.objects.prefetch_related('articles').all()

    @classmethod
    def search_faqs(cls, query):
        cls.ensure_seeded_faqs()
        if not query:
            return FAQArticle.objects.filter(is_published=True)[:20]

        q = query.strip()
        return FAQArticle.objects.filter(
            models.Q(question__icontains=q) |
            models.Q(answer__icontains=q) |
            models.Q(keywords__icontains=q),
            is_published=True
        )[:20]

    @classmethod
    def vote_helpful(cls, article_id):
        art = FAQArticle.objects.filter(id=article_id).first()
        if art:
            art.helpful_count += 1
            art.save(update_fields=['helpful_count'])
            return True, art.helpful_count
        return False, 0

    @classmethod
    def ensure_seeded_faqs(cls):
        """Seeds authentic, comprehensive knowledgebase entries on initial setup."""
        if FAQCategory.objects.exists():
            return

        seed_data = [
            {
                'title': 'Shipping, Transit & Delivery',
                'slug': 'shipping-transit-delivery',
                'description': 'Carrier timeframes, expedited delivery, and real-time tracking.',
                'icon_name': 'truck',
                'order': 1,
                'articles': [
                    {
                        'question': 'How quickly will my order ship after payment authorization?',
                        'answer': 'Orders are routed instantly to warehouse fulfillment queues upon successful payment authorization. Standard courier orders ship within 24 to 48 hours. Expedited and Priority Same-Day orders receive immediate priority packing and courier dispatch within 4 business hours.',
                        'keywords': 'shipping speed, dispatch time, fulfillment, same-day'
                    },
                    {
                        'question': 'How do I track my delivery status and carrier checkpoint events?',
                        'answer': 'Visit your Orders page and select any active order. You will see an interactive 4-stage tracking stepper (Confirmed, Packed, Shipped, Delivered) alongside live carrier tracking numbers and GPS checkpoint timestamps.',
                        'keywords': 'track shipment, carrier tracking, tracking number, courier log'
                    },
                    {
                        'question': 'Can I request delivery to PO Boxes or APO/FPO addresses?',
                        'answer': 'Yes, Standard Insured Courier can deliver to all verified residential addresses and US postal stations. Expedited Air and Priority Same-Day require a physical street address with signature confirmation upon receipt.',
                        'keywords': 'po box, apo, international delivery, address validation'
                    }
                ]
            },
            {
                'title': 'Returns, RMAs & Exchanges',
                'slug': 'returns-rmas-exchanges',
                'description': '30-day money back guarantee, prepaid return labels, and replacements.',
                'icon_name': 'rotate-ccw',
                'order': 2,
                'articles': [
                    {
                        'question': 'What is the ShopSphere 30-Day Money-Back Guarantee?',
                        'answer': 'Every hardware purchase from verified merchants is backed by our 30-day hassle-free return policy. If you receive a defective unit or are dissatisfied with your hardware, you can generate a prepaid return label directly in the Returns portal.',
                        'keywords': 'return policy, money back guarantee, refund timeframe'
                    },
                    {
                        'question': 'How do I initiate a hardware return or request an exchange for another edition?',
                        'answer': 'Navigate to your Orders history and click "Return Item" next to the delivered line item. Choose between a full monetary refund to your original payment method or an instant Hardware Exchange for a different variant/SKU.',
                        'keywords': 'rma, initiate return, exchange variant, replacement'
                    },
                    {
                        'question': 'How long does it take to receive my refund after dropping off the package?',
                        'answer': 'Once the courier scans your return package at the drop-off facility, our inspection system triggers automated ledger settlement. Refunds typically reflect on your bank or credit card statement within 2 to 5 business days.',
                        'keywords': 'refund speed, bank deposit, returned item inspection'
                    }
                ]
            },
            {
                'title': 'Payment Vault & Tax Invoicing',
                'slug': 'payment-vault-tax-invoicing',
                'description': 'Credit cards, PCI-DSS tokenization, sales tax calculation, and printable receipts.',
                'icon_name': 'credit-card',
                'order': 3,
                'articles': [
                    {
                        'question': 'How does ShopSphere protect my saved payment card details?',
                        'answer': 'ShopSphere utilizes an isolated, PCI-DSS Level 1 compliant tokenization vault simulation. Your full 16-digit Primary Account Number (PAN) and CVV security code are never stored in raw database plaintext. Only tokenized references and masked 4-digit previews are retained.',
                        'keywords': 'pci dss, credit card security, tokenization, payment vault'
                    },
                    {
                        'question': 'Where can I find and download official tax invoices for my accounting?',
                        'answer': 'Click on any order in your Order History and select "Tax Invoice". Each invoice includes compliant VAT/EIN business tax identifiers, itemized line items, regional sales tax computations, and printer-friendly PDF layout.',
                        'keywords': 'tax invoice, printable receipt, vat, ein, business expense'
                    },
                    {
                        'question': 'How is sales tax calculated for multi-state deliveries?',
                        'answer': 'Sales tax is calculated at checkout based on the statutory state tax rate of the recipient delivery address (e.g. 8.25% in CA, 8.875% in NY) in accordance with interstate marketplace facilitator laws.',
                        'keywords': 'tax rate, sales tax, calculation, interstate tax'
                    }
                ]
            },
            {
                'title': 'Account Security & Two-Factor (2FA)',
                'slug': 'account-security-two-factor',
                'description': 'TOTP authenticators, backup codes, password reset, and GDPR privacy.',
                'icon_name': 'shield-check',
                'order': 4,
                'articles': [
                    {
                        'question': 'How do I set up Two-Factor Authentication (2FA) with Google Authenticator or 1Password?',
                        'answer': 'Go to your Profile and select Two-Factor Auth. ShopSphere will generate a 32-character base32 secret and 8 emergency backup codes. Scan the URI or enter the key into your authenticator app, then enter the 6-digit TOTP code to confirm activation.',
                        'keywords': '2fa, totp, google authenticator, 1password, multi-factor'
                    },
                    {
                        'question': 'What should I do if I lose access to my phone or authenticator app?',
                        'answer': 'During 2FA login, click "Use emergency backup code instead". Enter one of the single-use 8-character recovery codes generated during your initial setup to regain immediate access to your account.',
                        'keywords': 'lost phone, backup code, 2fa recovery, emergency login'
                    },
                    {
                        'question': 'How do I download my complete personal data archive under GDPR Article 20?',
                        'answer': 'Visit Profile → Privacy & GDPR. Click "Download My JSON Data Archive" to immediately download an export of your profile details, orders, addresses, reviews, and support logs in a portable JSON format.',
                        'keywords': 'gdpr, data portability, data export, json download'
                    }
                ]
            }
        ]

        for cat_data in seed_data:
            cat = FAQCategory.objects.create(
                title=cat_data['title'],
                slug=cat_data['slug'],
                description=cat_data['description'],
                icon_name=cat_data['icon_name'],
                display_order=cat_data['order']
            )
            for art in cat_data['articles']:
                FAQArticle.objects.create(
                    category=cat,
                    question=art['question'],
                    answer=art['answer'],
                    keywords=art['keywords'],
                    helpful_count=12
                )
