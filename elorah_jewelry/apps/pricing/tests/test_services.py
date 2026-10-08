from django.test import TestCase
from decimal import Decimal
from apps.catalog.models import Material, Purity, Category, Product
from apps.pricing.models import MetalRate, GSTConfig
from apps.pricing.services import PricingService, TaxService, MetalRateNotFound
from apps.core.models import SiteConfig
from django.core.cache import cache

class PricingServiceTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteConfig.objects.create(store_state="Kerala")
        self.material = Material.objects.create(name="Gold")
        self.purity = Purity.objects.create(material=self.material, name="22K")
        self.category = Category.objects.create(name="Rings", slug="rings")
        
        self.rate = MetalRate.objects.create(
            material=self.material,
            purity=self.purity,
            rate_per_gram=Decimal("5000.00"),
            effective_date="2026-01-01",
            is_current=True
        )

        self.gst = GSTConfig.objects.create(
            name="Jewelry GST",
            hsn_code="7113",
            tax_rate=Decimal("3.00"),
            effective_from="2026-01-01"
        )

        self.product_dynamic = Product.objects.create(
            name="Dynamic Ring",
            sku="DYN-1",
            category=self.category,
            material=self.material,
            purity=self.purity,
            pricing_mode="DYNAMIC",
            net_weight=Decimal("10.000"),
            making_charge_type="PER_GRAM",
            making_charge_value=Decimal("500.00"),
            stone_charge=Decimal("1000.00"),
            hsn_code="7113"
        )

    def test_get_current_rate(self):
        rate = PricingService.get_current_rate(self.material.id, self.purity.id)
        self.assertEqual(rate, Decimal("5000.00"))

    def test_dynamic_pricing_calculation(self):
        breakdown = PricingService.compute_price(self.product_dynamic, buyer_state="Kerala")
        
        # Metal Cost: 10g * 5000 = 50000
        self.assertEqual(breakdown.metal_cost, Decimal("50000.00"))
        # Making Charge: 10g * 500 = 5000
        self.assertEqual(breakdown.making_charge, Decimal("5000.00"))
        # Base Price: 50000 + 5000 + 1000 = 56000
        self.assertEqual(breakdown.base_price, Decimal("56000.00"))
        # GST: 3% of 56000 = 1680
        self.assertEqual(breakdown.tax_amount, Decimal("1680.00"))
        # Intra-state (Kerala), so CGST=840, SGST=840, IGST=0
        self.assertEqual(breakdown.cgst, Decimal("840.00"))
        self.assertEqual(breakdown.sgst, Decimal("840.00"))
        self.assertEqual(breakdown.igst, Decimal("0.00"))
        # Final Price: 56000 + 1680 = 57680
        self.assertEqual(breakdown.final_price, Decimal("57680.00"))
