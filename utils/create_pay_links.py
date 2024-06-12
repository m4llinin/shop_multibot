import aiohttp
from config.config import PRODAMUS_LINK, BASE_URL
from .Cart import Cart


async def create_pay_link(cart: Cart = None):
    url = (F"{PRODAMUS_LINK}/?order_id={cart.order_id}&products[0][price]={cart.good.price * cart.extra_charge}"
           F"&products[0][quantity]={cart.count}&products[0][sku]={cart.good.id}&sys=coin&"
           F"products[0][name]={cart.good.name.replace(' ', '%20')}&do=link&"
           F"urlNotification={BASE_URL}/prodamus&customer_extra={cart.shop_name}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def create_pay_link_balance(amount: int, order_id: int, shop_name: str):
    url = (F"{PRODAMUS_LINK}/?order_id={order_id}&products[0][price]={amount}"
           F"&products[0][quantity]=1&sys=coin&products[0][name]=Пополнение%20баланса%20на%20{amount}&do=link&"
           F"urlNotification={BASE_URL}/prodamus/balance&customer_extra={shop_name}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
