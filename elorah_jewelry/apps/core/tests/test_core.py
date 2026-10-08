from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import SiteConfig
from apps.core.utils import format_inr

class CoreTests(TestCase):
    def test_health_check(self):
        c = Client()
        response = c.get(reverse('core:health-check'))
        # Depending on if DB/Redis are up, it might be 200 or 503, but it shouldn't crash
        self.assertIn(response.status_code, [200, 503])
        self.assertIn('status', response.json())

    def test_format_inr(self):
        self.assertEqual(format_inr(123456.50), "?1,23,456.50")

    def test_site_config_singleton(self):
        c1 = SiteConfig.get()
        c2 = SiteConfig.get()
        self.assertEqual(c1.pk, 1)
        self.assertEqual(c1.pk, c2.pk)
        
        # Manually create another, it should overwrite/fail depending on impl
        c3 = SiteConfig.objects.create(store_name="Test")
        self.assertEqual(c3.pk, 1)
