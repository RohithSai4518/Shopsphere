import unittest
from unittest import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from apps.rbac.models import Role, Permission, RolePermission
from apps.rbac.decorators import role_required

User = get_user_model()

class RbacTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User.objects.create_user(email='admin@test.com', username='admin@test.com', password='Pass', role='ADMIN')
        self.customer = User.objects.create_user(email='cust@test.com', username='cust@test.com', password='Pass', role='CUSTOMER')

    def test_role_required_decorator_allowed(self):
        @role_required('ADMIN')
        def mock_view(request):
            return "SUCCESS"

        request = self.factory.get('/')
        request.user = self.admin

        response = mock_view(request)
        self.assertEqual(response, "SUCCESS")

    def test_role_required_decorator_denied(self):
        @role_required('ADMIN')
        def mock_view(request):
            return "SUCCESS"

        request = self.factory.get('/')
        request.user = self.customer

        # Attach Session and Messages Middleware
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        msg_middleware = MessageMiddleware(lambda req: None)
        msg_middleware.process_request(request)

        response = mock_view(request)
        self.assertEqual(response.status_code, 302)
