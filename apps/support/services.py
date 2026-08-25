import random
from .models import SupportTicket, SupportMessage, SupportSatisfactionRating
from apps.notifications.services import NotificationService

class SupportService:
    @staticmethod
    def create_ticket(user, subject, category='GENERAL', priority='MEDIUM', initial_message=None, order=None):
        ticket_number = f"TKT-{random.randint(10000, 99999)}"
        ticket = SupportTicket.objects.create(
            ticket_number=ticket_number,
            user=user,
            order=order,
            subject=subject,
            category=category,
            priority=priority,
            status='OPEN'
        )

        if initial_message:
            SupportMessage.objects.create(
                ticket=ticket,
                sender=user,
                message=initial_message
            )

        return ticket

    @staticmethod
    def add_message(ticket, sender, message, is_internal_note=False):
        msg = SupportMessage.objects.create(
            ticket=ticket,
            sender=sender,
            message=message,
            is_internal_note=is_internal_note
        )

        if sender != ticket.user:
            ticket.status = 'IN_PROGRESS'
            ticket.save()

            NotificationService.send_notification(
                user=ticket.user,
                title=f"New Reply on Ticket #{ticket.ticket_number}",
                message=f"Support agent replied: '{message[:60]}...'",
                notification_type='SUPPORT',
                action_url=f"/support/{ticket.id}/"
            )
        return msg

    @staticmethod
    def escalate_ticket(ticket, new_priority='URGENT'):
        ticket.priority = new_priority
        ticket.save()

        NotificationService.send_notification(
            user=ticket.user,
            title=f"Support Ticket #{ticket.ticket_number} Escalated",
            message=f"Your ticket '{ticket.subject}' has been escalated to {new_priority} priority for rapid agent response.",
            notification_type='SUPPORT'
        )

        return ticket

    @staticmethod
    def submit_csat(ticket, user, rating_score, feedback_text=None):
        csat, _ = SupportSatisfactionRating.objects.update_or_create(
            ticket=ticket,
            user=user,
            defaults={'rating_score': rating_score, 'feedback_text': feedback_text}
        )
        ticket.status = 'CLOSED'
        ticket.save()
        return csat
