from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta
from .models import Order, OrderItem, OrderStatusHistory, Shipment, ShipmentEvent, ExchangeRequest
from apps.inventory.services import InventoryService, InsufficientStockError
from apps.payments.services import PaymentSandboxService
from apps.notifications.services import NotificationService
from apps.audit.models import SecurityAuditLog

class OrderProcessingError(Exception):
    pass

class OrderService:
    @staticmethod
    @transaction.atomic
    def process_checkout(user, cart_items, shipping_address, coupon=None):
        if not cart_items:
            raise OrderProcessingError("Cannot process checkout for an empty cart.")

        subtotal = sum(Decimal(str(item.subtotal)) for item in cart_items)
        discount_amount = Decimal('0.00')
        if coupon:
            discount_amount = coupon.calculate_discount(subtotal)

        taxable = max(Decimal('0.00'), subtotal - discount_amount)
        tax_amount = round(taxable * Decimal('0.0825'), 2)
        total_amount = round(taxable + tax_amount, 2)

        order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        est_delivery = timezone.now().date() + timedelta(days=3)

        order = Order.objects.create(
            order_number=order_number,
            user=user,
            status='CONFIRMED',
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_amount=Decimal('0.00'),
            discount_amount=discount_amount,
            total_amount=total_amount,
            coupon=coupon,
            shipping_address_json=shipping_address,
            estimated_delivery_date=est_delivery
        )

        OrderStatusHistory.objects.create(
            order=order,
            from_status='PENDING',
            to_status='CONFIRMED',
            changed_by=user,
            notes='Order created & payment authorized successfully.'
        )

        for ci in cart_items:
            # Stock Reservation
            try:
                InventoryService.reserve_stock(ci.variant, ci.quantity, reference_id=order.id)
            except InsufficientStockError as err:
                raise OrderProcessingError(str(err))

            OrderItem.objects.create(
                order=order,
                variant=ci.variant,
                seller=ci.variant.product.seller,
                unit_price=ci.effective_unit_price,
                quantity=ci.quantity,
                total_price=ci.subtotal,
                item_status='PENDING'
            )

        # Payment Authorization Sandbox
        PaymentSandboxService.authorize_and_charge(order)

        # Clear Cart
        cart_items.delete()

        # Dispatch Notification
        NotificationService.send_notification(
            user=user,
            title=f"Order Confirmed: #{order.order_number}",
            message=f"Thank you for your order of ${total_amount}! Estimated delivery: {est_delivery}.",
            notification_type='ORDER',
            action_url=f"/orders/{order.id}/"
        )

        SecurityAuditLog.objects.create(
            user=user,
            action='CHECKOUT_SUCCESS',
            module='orders',
            entity_type='Order',
            entity_id=order.id,
            metadata_json=f'{{"order_number": "{order.order_number}", "total": {total_amount}}}'
        )

        return order

    @staticmethod
    @transaction.atomic
    def update_order_status(order, new_status, user=None, notes=None):
        valid_transitions = {
            'PENDING': ['CONFIRMED', 'CANCELLED'],
            'CONFIRMED': ['PACKED', 'PROCESSING', 'CANCELLED'],
            'PACKED': ['SHIPPED', 'CANCELLED'],
            'PROCESSING': ['SHIPPED', 'CANCELLED'],
            'SHIPPED': ['OUT_FOR_DELIVERY', 'DELIVERED'],
            'OUT_FOR_DELIVERY': ['DELIVERED'],
            'DELIVERED': ['RETURN_REQUESTED', 'RETURNED'],
            'RETURN_REQUESTED': ['RETURNED', 'DELIVERED'],
            'CANCELLED': [],
            'RETURNED': ['REFUNDED'],
            'REFUNDED': []
        }

        current_status = order.status
        allowed = valid_transitions.get(current_status, [])
        if new_status not in allowed:
            raise OrderProcessingError(f"Invalid status transition from '{current_status}' to '{new_status}'.")

        order.status = new_status
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            from_status=current_status,
            to_status=new_status,
            changed_by=user,
            notes=notes or f"Status updated to {new_status}"
        )

        # Handle cancellation stock release
        if new_status == 'CANCELLED':
            for item in order.items.all():
                InventoryService.release_stock_reservation(item.variant, item.quantity, reference_id=order.id)
                item.item_status = 'CANCELLED'
                item.save()

        NotificationService.send_notification(
            user=order.user,
            title=f"Order Status Update: #{order.order_number}",
            message=f"Your order #{order.order_number} status is now '{new_status}'.",
            notification_type='ORDER',
            action_url=f"/orders/{order.id}/"
        )

        return order

    @staticmethod
    @transaction.atomic
    def create_shipment(order, carrier, tracking_number):
        shipment = Shipment.objects.create(
            order=order,
            carrier=carrier,
            tracking_number=tracking_number,
            status='IN_TRANSIT',
            shipped_at=timezone.now()
        )

        ShipmentEvent.objects.create(
            shipment=shipment,
            location='Logistics Warehouse',
            status_description='Package picked up by carrier',
            event_timestamp=timezone.now()
        )

        OrderService.update_order_status(order, 'SHIPPED')
        return shipment
