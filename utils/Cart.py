from dataclasses import dataclass

from database.schemas.Good import Good


@dataclass
class Cart:
    good: Good = None
    total_price: int | float = 0
    extra_charge: int = 1
    count: int = 1
    order_id: int = 0
    shop_name: str = ""
