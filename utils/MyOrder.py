from dataclasses import dataclass

from database.schemas.Order import Order


@dataclass
class MyOrder:
    orders: list[Order]
    all_pages: int
    cur_page: int = 1
