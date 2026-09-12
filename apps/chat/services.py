from django.utils import timezone
from .models import ChatChannel, ChatMessage, BotKnowledgeRule
from apps.orders.models import Order

class ChatEngine:
    """
    Manages channel lifecycle, agent queueing, and message dispatching.
    """

    @classmethod
    def get_or_create_support_channel(cls, customer, order=None):
        channel = ChatChannel.objects.filter(
            customer=customer,
            status__in=['OPEN', 'WAITING_ON_AGENT', 'WAITING_ON_CUSTOMER']
        ).first()

        if not channel:
            channel = ChatChannel.objects.create(
                customer=customer,
                order=order,
                channel_type='SUPPORT_TRIAGE',
                subject=f"Assistance for Order #{order.order_number}" if order else "General Customer Support",
                status='OPEN'
            )
            # Welcome greeting from virtual assistant
            ChatMessage.objects.create(
                channel=channel,
                sender=None,
                sender_role='AI_BOT',
                body="Hello! I'm ShopSphere's virtual support assistant. How can I help you today? You can ask about tracking, returns, cancellations, or request to speak with a human specialist."
            )

        return channel

    @classmethod
    def post_user_message(cls, channel, user, message_text):
        msg = ChatMessage.objects.create(
            channel=channel,
            sender=user,
            sender_role='CUSTOMER',
            body=message_text
        )
        channel.updated_at = timezone.now()
        channel.save()

        # Execute automated bot triage
        BotTriageAssistant.process_incoming_message(channel, message_text)
        return msg


class BotTriageAssistant:
    """
    Evaluates incoming customer queries against knowledgebase intent rules,
    injects live order data, and routes to human agents when required.
    """

    DEFAULT_RULES = [
        {
            'intent_tag': 'ORDER_TRACKING',
            'keyword_triggers': 'track, where is my order, status, delivery, tracking, eta',
            'automated_response': "You can view live checkpoint updates by visiting our Parcel Tracking Portal at /logistics/track/. If you share your tracking number here, I can also check its milestone status for you!",
            'escalate': False
        },
        {
            'intent_tag': 'RETURNS_REFUND',
            'keyword_triggers': 'return, refund, exchange, defective, damaged, wrong item',
            'automated_response': "ShopSphere guarantees 30-day hassle-free returns. You can initiate a prepaid return label directly in your Order Details page. Once received, refunds are processed within 48 hours.",
            'escalate': False
        },
        {
            'intent_tag': 'HUMAN_AGENT_REQUEST',
            'keyword_triggers': 'human, agent, representative, operator, real person, supervisor',
            'automated_response': "I am routing you to our next available Live Support Specialist. Please hold while an agent joins this chat session.",
            'escalate': True
        },
        {
            'intent_tag': 'PRIME_MEMBERSHIP',
            'keyword_triggers': 'prime, membership, cashback, rewards, annual',
            'automated_response': "ShopSphere Prime gives you unlimited free 1-day delivery and 5% back on all purchases! Explore plan tiers at /memberships/prime/.",
            'escalate': False
        }
    ]

    @classmethod
    def seed_default_rules(cls):
        for r in cls.DEFAULT_RULES:
            BotKnowledgeRule.objects.get_or_create(
                intent_tag=r['intent_tag'],
                defaults={
                    'keyword_triggers': r['keyword_triggers'],
                    'automated_response': r['automated_response'],
                    'should_escalate_to_human': r['escalate']
                }
            )

    @classmethod
    def process_incoming_message(cls, channel, text):
        cls.seed_default_rules()
        rules = BotKnowledgeRule.objects.filter(is_active=True)

        matched_rule = None
        for r in rules:
            if r.matches(text):
                matched_rule = r
                break

        if matched_rule:
            reply_text = matched_rule.automated_response

            # Enhance tracking replies if channel has an attached order
            if matched_rule.intent_tag == 'ORDER_TRACKING' and channel.order:
                reply_text += f"\n\n[Order #{channel.order.order_number} Current Status: {channel.order.get_status_display()}]"

            ChatMessage.objects.create(
                channel=channel,
                sender=None,
                sender_role='AI_BOT',
                body=reply_text
            )

            if matched_rule.should_escalate_to_human:
                channel.status = 'WAITING_ON_AGENT'
                channel.save()
        else:
            # Fallback reply
            ChatMessage.objects.create(
                channel=channel,
                sender=None,
                sender_role='AI_BOT',
                body="Thank you for your message! If you need help with a specific order, tracking number, or return, let me know. Or type 'human agent' to speak with our support team."
            )
