import unittest
from unittest import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from apps.accounts.models import User
from apps.orders.models import Order
from apps.chat.models import ChatChannel, ChatMessage, BotKnowledgeRule
from apps.chat.services import ChatEngine, BotTriageAssistant

class ChatSubsystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='chat_customer@example.com',
            email='chat_customer@example.com',
            password='Password123!'
        )
        self.agent = User.objects.create_user(
            username='support_rep@example.com',
            email='support_rep@example.com',
            password='Password123!',
            role='SUPPORT'
        )
        self.order = Order.objects.create(
            order_number='ORD-CHAT-5544',
            user=self.user,
            status='SHIPPED',
            subtotal=Decimal('50.00'),
            tax_amount=Decimal('4.00'),
            shipping_amount=Decimal('0.00'),
            total_amount=Decimal('54.00')
        )
        BotTriageAssistant.seed_default_rules()

    def test_channel_creation_with_welcome_message(self):
        channel = ChatEngine.get_or_create_support_channel(self.user, order=self.order)
        self.assertEqual(channel.customer, self.user)
        self.assertEqual(channel.order, self.order)
        self.assertEqual(channel.messages.count(), 1)
        welcome = channel.messages.first()
        self.assertEqual(welcome.sender_role, 'AI_BOT')

    def test_bot_triage_tracking_intent(self):
        channel = ChatEngine.get_or_create_support_channel(self.user, order=self.order)
        # Customer asks where is order
        ChatEngine.post_user_message(channel, self.user, "Hi, where is my order right now?")

        # 1 initial welcome + 1 user msg + 1 bot reply = 3
        self.assertEqual(channel.messages.count(), 3)
        bot_reply = channel.messages.last()
        self.assertEqual(bot_reply.sender_role, 'AI_BOT')
        self.assertIn("Parcel Tracking Portal", bot_reply.body)
        self.assertIn("ORD-CHAT-5544", bot_reply.body)

    def test_human_agent_escalation(self):
        channel = ChatEngine.get_or_create_support_channel(self.user)
        self.assertEqual(channel.status, 'OPEN')

        # Customer explicitly requests human agent
        ChatEngine.post_user_message(channel, self.user, "I need to talk to a human agent please")
        channel.refresh_from_db()
        self.assertEqual(channel.status, 'WAITING_ON_AGENT')
        bot_reply = ChatMessage.objects.filter(channel=channel, sender_role='AI_BOT', body__icontains='Live Support Specialist').first()
        self.assertIsNotNone(bot_reply)
        self.assertIn("routing you to our next available Live Support Specialist", bot_reply.body)

    def test_chat_views_and_polling_api(self):
        self.client.force_login(self.user)
        channel = ChatEngine.get_or_create_support_channel(self.user)

        # Chat room page
        resp_room = self.client.get(reverse('chat:chat_room_detail', args=[channel.channel_code]))
        self.assertEqual(resp_room.status_code, 200)
        self.assertContains(resp_room, 'ShopSphere 24/7 Virtual Support')

        # Send message via API
        resp_send = self.client.post(
            reverse('chat:api_send_message', args=[channel.channel_code]),
            {'body': 'How do I initiate a return?'}
        )
        self.assertEqual(resp_send.status_code, 302)

        # Poll messages
        resp_poll = self.client.get(reverse('chat:api_poll_messages', args=[channel.channel_code]))
        self.assertEqual(resp_poll.status_code, 200)
        data = resp_poll.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['messages']) >= 2)

        # Agent workspace view
        self.client.force_login(self.agent)
        resp_agent = self.client.get(reverse('chat:agent_workspace'))
        self.assertEqual(resp_agent.status_code, 200)
        self.assertContains(resp_agent, 'Support Agent Workspace')
