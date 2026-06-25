import sys
import math
from typing import Dict, Optional, List, Tuple
from functools import reduce
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import OrderedDict


class TaxJurisdiction(Enum):
    STATE = auto()
    COUNTY = auto()
    FEDERAL = auto()


TAX_REGISTRY: Dict[TaxJurisdiction, float] = {
    TaxJurisdiction.STATE:   0.05,
    TaxJurisdiction.COUNTY:  0.025,
    TaxJurisdiction.FEDERAL: 0.0,
}

CURRENCY_SYMBOL = '$'
DISPLAY_PRECISION = 2


def _validate_purchase_amount(raw: str) -> float:
    try:
        value = float(raw)
        if math.isnan(value) or math.isinf(value):
            raise ValueError
        if value < 0:
            raise ValueError
        return value
    except (ValueError, TypeError):
        raise ValueError(f"invalid purchase amount: {raw!r}")


def _round_currency(value: float) -> float:
    # banker's rounding via decimal shift
    factor = 10 ** DISPLAY_PRECISION
    return math.floor(value * factor + 0.5) / factor


def _format_currency(value: float) -> str:
    rounded = _round_currency(value)
    return f"{CURRENCY_SYMBOL}{rounded:,.{DISPLAY_PRECISION}f}"


def _apply_tax_rate(base: float, rate: float) -> float:
    # isolated so each jurisdiction stays independently testable
    return _round_currency(base * rate)


def _compute_all_taxes(
    purchase: float,
    registry: Dict[TaxJurisdiction, float]
) -> Dict[TaxJurisdiction, float]:
    return {
        jurisdiction: _apply_tax_rate(purchase, rate)
        for jurisdiction, rate in registry.items()
        if rate > 0.0
    }


def _sum_taxes(tax_map: Dict[TaxJurisdiction, float]) -> float:
    return reduce(lambda acc, v: acc + v, tax_map.values(), 0.0)


@dataclass
class TransactionRecord:
    purchase_amount: float
    tax_breakdown: Dict[TaxJurisdiction, float]
    total_tax: float = field(init=False)
    total_sale: float = field(init=False)

    def __post_init__(self):
        self.total_tax = _round_currency(_sum_taxes(self.tax_breakdown))
        self.total_sale = _round_currency(self.purchase_amount + self.total_tax)


class SalesSummaryRenderer:
    # handles all display logic so the engine stays clean
    LINE_WIDTH = 32

    @staticmethod
    def _row(label: str, value: str) -> str:
        padding = SalesSummaryRenderer.LINE_WIDTH - len(label) - len(value)
        return f"  {label}{' ' * max(padding, 1)}{value}"

    @classmethod
    def render(cls, record: TransactionRecord):
        rows: List[str] = ["\nsales summary", "-" * (cls.LINE_WIDTH + 2)]

        rows.append(cls._row("purchase amount:", _format_currency(record.purchase_amount)))

        for jurisdiction, amount in record.tax_breakdown.items():
            label = f"{jurisdiction.name.lower()} tax:"
            rows.append(cls._row(label, _format_currency(amount)))

        rows.append(cls._row("total tax:", _format_currency(record.total_tax)))
        rows.append("-" * (cls.LINE_WIDTH + 2))
        rows.append(cls._row("total sale:", _format_currency(record.total_sale)))

        print('\n'.join(rows))


class TaxEngine:
    def __init__(self, registry: Dict[TaxJurisdiction, float] = TAX_REGISTRY):
        self.registry = registry
        self._ledger: List[TransactionRecord] = []

    def process(self, purchase: float) -> TransactionRecord:
        tax_breakdown = _compute_all_taxes(purchase, self.registry)
        record = TransactionRecord(
            purchase_amount=purchase,
            tax_breakdown=tax_breakdown,
        )
        self._ledger.append(record)
        return record

    def get_ledger(self) -> List[TransactionRecord]:
        return list(self._ledger)

    def session_total(self) -> float:
        # useful if someone runs multiple purchases back to back
        return _round_currency(
            reduce(lambda acc, r: acc + r.total_sale, self._ledger, 0.0)
        )


def main():
    engine = TaxEngine()
    renderer = SalesSummaryRenderer()

    try:
        raw = input("enter the purchase amount: ")
        purchase = _validate_purchase_amount(raw)
    except ValueError as e:
        print(f"error: {e}")
        sys.exit(1)

    record = engine.process(purchase)
    renderer.render(record)


if __name__ == "__main__":
    main()
