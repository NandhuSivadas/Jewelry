from django.test import TestCase
from django.db.utils import IntegrityError
from apps.catalog.models import Material, Purity, Category, Product

class CatalogModelTests(TestCase):
    def setUp(self):
        self.material = Material.objects.create(name="Gold")
        self.purity = Purity.objects.create(material=self.material, name="22K")
        self.category = Category.objects.create(name="Rings", slug="rings")
        
    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Ring",
            sku="R001",
            category=self.category,
            material=self.material,
            purity=self.purity,
            base_price=5000,
            pricing_mode="FIXED"
        )
        self.assertEqual(product.sku, "R001")
        self.assertTrue(product.is_active)
        self.assertEqual(product.slug, "test-ring")

    def test_negative_price_constraint(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Bad Ring",
                sku="R002",
                category=self.category,
                material=self.material,
                purity=self.purity,
                base_price=-100
            )
