from .models import Notification

class NotificationService:
    @staticmethod
    def send_notification(user, title, message, notification_type='ORDER'):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )

    @staticmethod
    def mark_all_as_read(user):
        return Notification.objects.filter(user=user, is_read=False).update(is_read=True)
