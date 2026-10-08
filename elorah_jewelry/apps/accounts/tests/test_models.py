from django.test import TestCase
from apps.accounts.models import CustomUser, UserProfile, Address

class AccountsModelTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123', first_name='Test', last_name='User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(email='admin@example.com', password='password123', first_name='Admin', last_name='User')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_email_verified)
