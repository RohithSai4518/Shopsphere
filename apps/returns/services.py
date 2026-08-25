from decimal import Decimal
from django.db import transaction
from .models import ReturnRequest
from apps.inventory.services import InventoryService
from apps.payments.models import Payment
from apps.payments.services import PaymentSandboxService
from apps.notifications.services import NotificationService
from apps.audit.models import SecurityAuditLog

class ReturnService:
    @staticmethod
    @transaction.atomic
    def submit_return_request(order, order_item, user, reason, comments=None):
        label_url = f"https://labels.shopsphere.local/rma-{order_item.id}.pdf"
        rma = ReturnRequest.objects.create(
            order=order,
            order_item=order_item,
            user=user,
            reason=reason,
            comments=comments,
            status='SUBMITTED',
            return_shipping_label_url=label_url
        )

        NotificationService.send_notification(
            user=user,
            title=f"RMA Return Submitted for Order #{order.order_number}",
            message=f"Your return request for '{order_item.variant.product.name}' has been submitted.",
            notification_type='RETURN',
            action_url=f"/returns/"
        )

        return rma

    @staticmethod
    @transaction.atomic
    def process_rma_approval(return_request, approved_by_user=None, restocking_fee_pct=Decimal('5.00')):
        original_price = Decimal(str(return_request.order_item.total_price))
        fee = round((original_price * restocking_fee_pct) / Decimal('100.00'), 2)
        refund_amount = original_price - fee

        return_request.status = 'APPROVED'
        return_request.restocking_fee = fee
        return_request.refund_amount = refund_amount
        return_request.save()

        # Restock Inventory
        InventoryService.restock_variant(
            variant=return_request.order_item.variant,
            quantity=return_request.order_item.quantity,
            notes=f"Restocked via RMA #{return_request.id}"
        )

        # Refund Payment
        payment = Payment.objects.filter(order=return_request.order, status__in=['SUCCESS', 'CAPTURED']).first()
        if payment:
            PaymentSandboxService.process_refund(payment, refund_amount)
            return_request.status = 'REFUNDED'
            return_request.save()

        NotificationService.send_notification(
            user=return_request.user,
            title=f"RMA Return Approved & Refunded",
            message=f"A refund of ${refund_amount} has been processed for your return of '{return_request.order_item.variant.product.name}'.",
            notification_type='RETURN'
        )

        if approved_by_user:
            SecurityAuditLog.objects.create(
                user=approved_by_user,
                action='RMA_APPROVAL',
                module='returns',
                entity_type='ReturnRequest',
                entity_id=return_request.id,
                metadata_json=f'{{"refund": {refund_amount}}}'
            )

        return return_request
