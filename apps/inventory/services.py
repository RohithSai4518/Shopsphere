from django.db import transaction
from .models import Inventory, InventoryTransaction, WarehouseLocation, PurchaseOrder, PurchaseOrderItem
from apps.audit.models import SecurityAuditLog
from apps.notifications.services import NotificationService

class InsufficientStockError(Exception):
    pass

class InventoryService:
    @staticmethod
    @transaction.atomic
    def restock_variant(variant, quantity, warehouse_code='WH-WEST-01', user=None, notes='Manual Restock'):
        inv, _ = Inventory.objects.get_or_create(variant=variant)
        inv.quantity_on_hand += quantity
        inv.save()

        tx = InventoryTransaction.objects.create(
            variant=variant,
            transaction_type='RECEIPT',
            quantity=quantity,
            reference_type='RESTOCK',
            reference_id=warehouse_code,
            notes=notes
        )

        if user:
            SecurityAuditLog.objects.create(
                user=user,
                action='INVENTORY_RESTOCK',
                module='inventory',
                entity_type='ProductVariant',
                entity_id=variant.id,
                metadata_json=f'{{"added_qty": {quantity}, "new_total": {inv.quantity_on_hand}}}'
            )

        # Notify back in stock alerts
        alerts = variant.stock_alerts.filter(is_notified=False)
        for alert in alerts:
            NotificationService.send_notification(
                user=alert.user,
                title=f"Back in Stock: {variant.product.name}",
                message=f"The item '{variant.product.name} ({variant.variant_name})' is now back in stock!",
                notification_type='STOCK_ALERT',
                action_url=f"/product/{variant.product.slug}/"
            )
            alert.is_notified = True
            alert.save()

        return inv

    @staticmethod
    @transaction.atomic
    def reserve_stock(variant, quantity, reference_id=''):
        inv, _ = Inventory.objects.get_or_create(variant=variant)
        if inv.quantity_available < quantity:
            raise InsufficientStockError(f"Insufficient available stock for SKU {variant.sku}.")

        inv.quantity_reserved += quantity
        inv.save()

        InventoryTransaction.objects.create(
            variant=variant,
            transaction_type='RESERVATION',
            quantity=quantity,
            reference_type='ORDER',
            reference_id=reference_id,
            notes='Stock reserved for order'
        )
        return inv

    @staticmethod
    @transaction.atomic
    def release_stock_reservation(variant, quantity, reference_id=''):
        inv = Inventory.objects.filter(variant=variant).first()
        if inv:
            inv.quantity_reserved = max(0, inv.quantity_reserved - quantity)
            inv.save()

            InventoryTransaction.objects.create(
                variant=variant,
                transaction_type='RELEASE',
                quantity=quantity,
                reference_type='ORDER_CANCEL',
                reference_id=reference_id,
                notes='Stock reservation released'
            )
        return inv

    @staticmethod
    @transaction.atomic
    def deduct_stock_for_shipment(variant, quantity, reference_id=''):
        inv = Inventory.objects.get(variant=variant)
        inv.quantity_reserved = max(0, inv.quantity_reserved - quantity)
        inv.quantity_on_hand = max(0, inv.quantity_on_hand - quantity)
        inv.save()

        InventoryTransaction.objects.create(
            variant=variant,
            transaction_type='DEDUCTION',
            quantity=quantity,
            reference_type='SHIPMENT',
            reference_id=reference_id,
            notes='Stock deducted for shipment fulfillment'
        )

        return inv

    @staticmethod
    @transaction.atomic
    def adjust_damaged_stock(variant, quantity, notes='Damage report'):
        inv = Inventory.objects.get(variant=variant)
        inv.quantity_damaged += quantity
        inv.save()

        InventoryTransaction.objects.create(
            variant=variant,
            transaction_type='DAMAGE_ADJUSTMENT',
            quantity=quantity,
            reference_type='DAMAGE',
            notes=notes
        )
        return inv

    @staticmethod
    @transaction.atomic
    def receive_purchase_order(purchase_order, user=None):
        purchase_order.status = 'RECEIVED'
        purchase_order.save()

        for item in purchase_order.items.all():
            item.quantity_received = item.quantity_ordered
            item.save()

            InventoryService.restock_variant(
                variant=item.variant,
                quantity=item.quantity_ordered,
                warehouse_code=purchase_order.warehouse.code,
                user=user,
                notes=f"PO Receipt #{purchase_order.po_number}"
            )

        return purchase_order
