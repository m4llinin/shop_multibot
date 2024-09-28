import aiohttp
from config.config import PRODAMUS_LINK, BASE_URL, client
from .Cart import Cart


async def create_pay_link(cart: Cart = None):
    url = (F"{PRODAMUS_LINK}/?order_id={cart.order_id}&products[0][price]={cart.good.price * cart.extra_charge}"
           F"&products[0][quantity]={cart.count}&products[0][sku]={cart.good.id}&sys=coin&"
           F"products[0][name]={'Онлайн обучение'.replace(' ', '%20')}&do=link&"
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


async def create_cryptopay_link(cart: Cart):
    rates = await client.get_exchange_rates()
    rate_ton_rub = None
    for rate in rates:
        if rate.source == "TON" and rate.target == "RUB":
            rate_ton_rub = rate.rate

    invoice = await client.create_invoice(
        amount=cart.good.price * cart.extra_charge * cart.count / rate_ton_rub,
        asset="TON",
        accepted_assets=["TON", "USDT", "BTC"],
        payload=f"{cart.order_id}",
        allow_anonymous=False
    )
    return invoice.bot_invoice_url
