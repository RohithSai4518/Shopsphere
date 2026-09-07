import json
from decimal import Decimal
from django.utils import timezone
from .models import Order, OrderInvoice

class InvoiceService:
    """
    Enterprise Invoicing & Tax Computation Engine.
    Generates compliant sales tax invoices with regional rate validation.
    """
    TAX_RATES = {
        'CA': Decimal('0.0825'),
        'NY': Decimal('0.08875'),
        'TX': Decimal('0.0825'),
        'FL': Decimal('0.0700'),
        'WA': Decimal('0.0650'),
        'DEFAULT': Decimal('0.0800'),
    }

    @classmethod
    def calculate_tax(cls, taxable_amount, state_code='DEFAULT'):
        """Computes sales tax based on delivery destination state code."""
        rate = cls.TAX_RATES.get((state_code or '').upper().strip(), cls.TAX_RATES['DEFAULT'])
        tax = taxable_amount * rate
        return round(tax, 2), rate

    @classmethod
    def generate_invoice_for_order(cls, order):
        """Creates or returns the official tax invoice for an order."""
        if hasattr(order, 'invoice'):
            return order.invoice

        inv_number = f"INV-{timezone.now().year}-{order.order_number.replace('ORD-', '')}"

        invoice = OrderInvoice.objects.create(
            order=order,
            invoice_number=inv_number,
            tax_identifier='US-EIN-94-3829101',
            subtotal_amount=order.subtotal,
            tax_amount=order.tax_amount,
            shipping_amount=order.shipping_amount + getattr(order, 'gift_wrap_fee', Decimal('0.00')),
            discount_amount=order.discount_amount,
            total_amount=order.total_amount
        )
        return invoice

    @classmethod
    def get_invoice_context(cls, order):
        """Builds formatted invoice data context for template rendering."""
        invoice = cls.generate_invoice_for_order(order)
        
        try:
            shipping_addr = json.loads(order.shipping_address_json) if isinstance(order.shipping_address_json, str) else order.shipping_address_json
        except Exception:
            shipping_addr = {}

        try:
            billing_addr = json.loads(order.billing_address_json) if isinstance(order.billing_address_json, str) and order.billing_address_json != '{}' else shipping_addr
        except Exception:
            billing_addr = shipping_addr

        line_items = []
        for it in order.items.select_related('variant', 'variant__product', 'seller').all():
            line_items.append({
                'name': it.variant.product.name,
                'variant_name': it.variant.variant_name,
                'sku': it.variant.sku,
                'seller_name': it.seller.business_name,
                'unit_price': it.unit_price,
                'quantity': it.quantity,
                'total_price': it.total_price
            })

        return {
            'order': order,
            'invoice': invoice,
            'shipping_addr': shipping_addr,
            'billing_addr': billing_addr,
            'line_items': line_items,
            'company': {
                'name': 'ShopSphere Global Marketplace, Inc.',
                'tax_id': 'US-EIN-94-3829101',
                'vat_reg': 'EU-OSS-98210398',
                'address': '500 Market Square, Suite 1400',
                'city_state': 'San Francisco, CA 94105',
                'support_email': 'billing@shopsphere.internal'
            }
        }
