import json
import uuid
from django.utils import timezone
from django.db import transaction
from .models import User, Address, UserPreference, SavedPaymentMethod, LoginHistory
from apps.audit.models import SecurityAuditLog

class PrivacyService:
    """
    GDPR / CCPA Data Privacy Service.
    Provides Article 20 Right to Data Portability and Article 17 Right to Erasure.
    """

    @staticmethod
    def generate_full_data_archive(user):
        """
        Compiles all customer data across every domain module into an
        auditable, portable JSON dictionary.
        """
        # 1. Profile information
        profile_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'role': user.role,
            'is_verified': user.is_verified,
            'status': user.status,
            'registered_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }

        # 2. Addresses
        addresses_data = []
        for addr in user.addresses.all():
            addresses_data.append({
                'address_id': addr.id,
                'address_type': addr.address_type,
                'full_name': addr.full_name,
                'street_1': addr.street_address_1,
                'street_2': addr.street_address_2,
                'city': addr.city,
                'state': addr.state,
                'postal_code': addr.postal_code,
                'country': addr.country,
                'is_default': addr.is_default
            })

        # 3. Preferences
        pref = getattr(user, 'preferences', None)
        preference_data = {
            'email_notifications': pref.email_notifications if pref else True,
            'sms_notifications': pref.sms_notifications if pref else False,
            'promotional_emails': pref.promotional_emails if pref else True,
            'theme': pref.theme if pref else 'DARK',
            'currency': pref.currency if pref else 'USD',
            'language': pref.language if pref else 'en-us'
        }

        # 4. Masked Payment Methods
        payment_methods_data = []
        for pm in user.saved_payment_methods.all():
            payment_methods_data.append({
                'id': pm.id,
                'card_brand': pm.card_brand,
                'last4': pm.last4,
                'expiry': f"{pm.expiry_month:02d}/{pm.expiry_year}",
                'is_default': pm.is_default,
                'created_at': pm.created_at.isoformat()
            })

        # 5. Orders & Line Items
        orders_data = []
        for order in user.orders.all():
            items = []
            for it in order.items.all():
                items.append({
                    'item_id': it.id,
                    'product_name': it.product_name,
                    'sku': it.sku,
                    'unit_price': str(it.unit_price),
                    'quantity': it.quantity,
                    'total_price': str(it.total_price)
                })
            orders_data.append({
                'order_number': order.order_number,
                'status': order.status,
                'payment_status': order.payment_status,
                'subtotal': str(order.subtotal_price),
                'tax': str(order.tax_amount),
                'shipping_fee': str(order.shipping_fee),
                'discount': str(order.discount_amount),
                'total_amount': str(order.total_amount),
                'shipping_address': order.shipping_address_snapshot,
                'created_at': order.created_at.isoformat(),
                'items': items
            })

        # 6. Customer Reviews
        reviews_data = []
        for rev in user.reviews.all():
            reviews_data.append({
                'product_name': rev.product.name,
                'rating': rev.rating,
                'title': rev.title,
                'comment': rev.comment,
                'created_at': rev.created_at.isoformat()
            })

        # 7. Q&A Contributions
        questions_data = [
            {'question_text': q.question_text, 'product': q.product.name, 'created_at': q.created_at.isoformat()}
            for q in (user.product_questions.all() if hasattr(user, 'product_questions') else [])
        ]
        answers_data = [
            {'answer_text': a.answer_text, 'question': a.question.question_text, 'created_at': a.created_at.isoformat()}
            for a in (user.product_answers.all() if hasattr(user, 'product_answers') else [])
        ]

        # 8. Support Tickets
        tickets_data = []
        tickets_qs = user.support_tickets.all() if hasattr(user, 'support_tickets') else []
        for ticket in tickets_qs:
            tickets_data.append({
                'ticket_number': ticket.ticket_number,
                'subject': ticket.subject,
                'status': ticket.status,
                'priority': ticket.priority,
                'created_at': ticket.created_at.isoformat()
            })

        # 9. Return Requests (RMAs)
        returns_data = []
        for ret in getattr(user, 'return_requests', []).all() if hasattr(user, 'return_requests') else []:
            returns_data.append({
                'return_number': ret.return_number,
                'status': ret.status,
                'reason': ret.reason,
                'refund_amount': str(ret.refund_amount),
                'created_at': ret.created_at.isoformat()
            })

        # 10. Login History (Past 50 records)
        logins_data = [
            {'ip_address': log.ip_address, 'status': log.status, 'timestamp': log.created_at.isoformat()}
            for log in user.login_history.all()[:50]
        ]

        archive = {
            'gdpr_export_metadata': {
                'exported_at': timezone.now().isoformat(),
                'platform': 'ShopSphere Global Marketplace',
                'compliance_framework': 'GDPR (EU) 2016/679 / CCPA 2018',
                'data_subject_email': user.email
            },
            'profile': profile_data,
            'preferences': preference_data,
            'addresses': addresses_data,
            'payment_methods': payment_methods_data,
            'orders': orders_data,
            'reviews': reviews_data,
            'community_qa': {
                'questions': questions_data,
                'answers': answers_data
            },
            'support_tickets': tickets_data,
            'returns': returns_data,
            'login_history': logins_data
        }

        SecurityAuditLog.objects.create(
            user=user,
            action='DATA_PORTABILITY_EXPORT_GENERATED',
            module='accounts'
        )

        return archive

    @staticmethod
    @transaction.atomic
    def execute_right_to_be_forgotten(user, reason="User requested account erasure under GDPR Article 17"):
        """
        Permanently anonymizes personal identifiers while preserving financial
        invoicing compliance records.
        """
        anon_id = uuid.uuid4().hex[:10]
        original_email = user.email

        # 1. Scrub personal data
        user.first_name = "Anonymized"
        user.last_name = f"User_{anon_id}"
        user.email = f"erased_{anon_id}@anonymized.shopsphere.internal"
        user.username = f"erased_{anon_id}"
        user.phone = None
        user.is_active = False
        user.status = 'ERASED'
        user.set_unusable_password()
        user.save()

        # 2. Scrub addresses
        user.addresses.all().delete()

        # 3. Scrub saved payment cards
        user.saved_payment_methods.all().delete()

        # 4. Revoke active sessions
        user.active_sessions.all().delete()

        # 5. Log audit trail
        SecurityAuditLog.objects.create(
            action='ACCOUNT_ERASURE_COMPLETED',
            module='accounts',
            metadata_json=f'{{"anonymized_id": "{anon_id}", "reason": "{reason}"}}'
        )

        return True, "Your account has been permanently anonymized and personal identifiers removed."
