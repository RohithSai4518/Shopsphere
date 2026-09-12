import unittest
from unittest import TestCase
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.notifications.services import NotificationService

User = get_user_model()

class NotificationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='ntf@example.com', username='ntf@example.com', password='Password123!')

    def test_notification_service_send(self):
        ntf = NotificationService.send_notification(
            user=self.user,
            title='Order Shipped',
            message='Your order #ORD-1001 has been shipped.',
            notification_type='ORDER'
        )
        self.assertEqual(ntf.title, 'Order Shipped')
        self.assertFalse(ntf.is_read)

        NotificationService.mark_all_as_read(self.user)
        ntf.refresh_from_db()
        self.assertTrue(ntf.is_read)
