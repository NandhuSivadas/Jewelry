from dataclasses import dataclass
from decimal import Decimal
from django.core.cache import cache
from django.utils import timezone
from apps.pricing.models import MetalRate, GSTConfig

@dataclass
class TaxBreakdown:
    tax_rate: Decimal
    tax_amount: Decimal
    cgst: Decimal
    sgst: Decimal
    igst: Decimal
    total: Decimal

@dataclass
class PriceBreakdown:
    metal_cost: Decimal
    making_charge: Decimal
    stone_charge: Decimal
    base_price: Decimal
    discount_amount: Decimal
    pre_tax_price: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    cgst: Decimal
    sgst: Decimal
    igst: Decimal
    final_price: Decimal
    price_adjustment: Decimal
    total: Decimal

class MetalRateNotFound(Exception):
    pass

class TaxService:
    @staticmethod
    def get_active_gst_rate(hsn_code: str, applies_to: str = "TOTAL") -> Decimal:
        cache_key = f"gst_rate:{hsn_code}:{applies_to}"
        rate = cache.get(cache_key)
        if rate is not None:
            return rate
        
        today = timezone.localdate()
        config = GSTConfig.objects.filter(
            hsn_code=hsn_code,
            applies_to=applies_to,
            is_active=True,
            effective_from__lte=today
        ).exclude(
            effective_to__lt=today
        ).order_by('-effective_from').first()
        
        if config:
            rate = config.tax_rate
            cache.set(cache_key, rate, timeout=3600)
            return rate
        
        return Decimal("0.0")

    @staticmethod
    def compute(amount: Decimal, hsn_code: str, buyer_state: str = None) -> TaxBreakdown:
        tax_rate = TaxService.get_active_gst_rate(hsn_code)
        tax_amount = (amount * (tax_rate / Decimal("100"))).quantize(Decimal("0.01"))
        
        from apps.core.models import SiteConfig
        store_state = SiteConfig.get().store_state
        
        if buyer_state and buyer_state.lower() == store_state.lower():
            # Intra-state
            cgst = (tax_amount / 2).quantize(Decimal("0.01"))
            sgst = tax_amount - cgst
            igst = Decimal("0.00")
        else:
            # Inter-state
            cgst = Decimal("0.00")
            sgst = Decimal("0.00")
            igst = tax_amount
            
        return TaxBreakdown(
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            cgst=cgst,
            sgst=sgst,
            igst=igst,
            total=tax_amount
        )

class PricingService:
    @staticmethod
    def get_current_rate(material_id: int, purity_id: int) -> Decimal:
        cache_key = f"metal_rate:{material_id}:{purity_id}"
        rate = cache.get(cache_key)
        if rate is not None:
            return rate
            
        rate_val = MetalRate.objects.filter(
            material_id=material_id,
            purity_id=purity_id,
            is_current=True
        ).values_list('rate_per_gram', flat=True).first()
        
        if rate_val is None:
            raise MetalRateNotFound(f"No current rate for material {material_id}, purity {purity_id}")
            
        cache.set(cache_key, rate_val, timeout=3600)
        return rate_val

    @staticmethod
    def _compute_making_charge(product, metal_cost: Decimal) -> Decimal:
        if product.making_charge_type == "FIXED":
            return product.making_charge_value
        elif product.making_charge_type == "PER_GRAM":
            return (product.making_charge_value * (product.net_weight or Decimal("0"))).quantize(Decimal("0.01"))
        elif product.making_charge_type == "PERCENTAGE":
            return (metal_cost * (product.making_charge_value / Decimal("100"))).quantize(Decimal("0.01"))
        return Decimal("0.00")

    @staticmethod
    def compute_price(product, variant=None, buyer_state: str = None) -> PriceBreakdown:
        if product.pricing_mode == "FIXED":
            base_price = product.base_price
            metal_cost = Decimal("0.00")
            making_charge = Decimal("0.00")
        else:
            rate = PricingService.get_current_rate(product.material_id, product.purity_id)
            weight = variant.weight_adjustment if (variant and variant.weight_adjustment) else product.net_weight
            if not weight:
                weight = Decimal("0.00")
            metal_cost = (weight * rate).quantize(Decimal("0.01"))
            making_charge = PricingService._compute_making_charge(product, metal_cost)
            base_price = metal_cost + making_charge + product.stone_charge
            
        discount_amount = (base_price * (product.discount_percentage / Decimal("100"))).quantize(Decimal("0.01"))
        pre_tax_price = base_price - discount_amount
        
        tax = TaxService.compute(pre_tax_price, product.hsn_code, buyer_state)
        
        price_adjustment = variant.price_adjustment if variant else Decimal("0.00")
        final_price = pre_tax_price + tax.total
        total = final_price + price_adjustment
        
        return PriceBreakdown(
            metal_cost=metal_cost,
            making_charge=making_charge,
            stone_charge=product.stone_charge,
            base_price=base_price,
            discount_amount=discount_amount,
            pre_tax_price=pre_tax_price,
            tax_rate=tax.tax_rate,
            tax_amount=tax.tax_amount,
            cgst=tax.cgst,
            sgst=tax.sgst,
            igst=tax.igst,
            final_price=final_price,
            price_adjustment=price_adjustment,
            total=total
        )

    @staticmethod
    def snapshot_for_order(product, variant=None, buyer_state: str = None) -> dict:
        breakdown = PricingService.compute_price(product, variant, buyer_state)
        return {
            "metal_cost": str(breakdown.metal_cost),
            "making_charge": str(breakdown.making_charge),
            "stone_charge": str(breakdown.stone_charge),
            "base_price": str(breakdown.base_price),
            "discount_amount": str(breakdown.discount_amount),
            "pre_tax_price": str(breakdown.pre_tax_price),
            "tax_rate": str(breakdown.tax_rate),
            "tax_amount": str(breakdown.tax_amount),
            "cgst": str(breakdown.cgst),
            "sgst": str(breakdown.sgst),
            "igst": str(breakdown.igst),
            "final_price": str(breakdown.final_price),
            "price_adjustment": str(breakdown.price_adjustment),
            "total": str(breakdown.total)
        }

    @staticmethod
    def invalidate_rate_cache(material_id: int, purity_id: int) -> None:
        cache.delete(f"metal_rate:{material_id}:{purity_id}")
