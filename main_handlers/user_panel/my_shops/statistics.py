import calendar
from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.schemas.Shop import Shop
from utils import load_texts
from keyboards import InlineKeyboardMain

from config.config import TZ
from database.commands import Database


async def statistics(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")
    period, shop_id = int(callback.data.split("_")[1]), int(callback.data.split("_")[2])

    now = datetime.now(tz=TZ)
    if period == 1:
        start = datetime(now.year, now.month, now.day, 0, 0, 0)
        end = datetime(now.year, now.month, now.day, 23, 59, 59)
    elif period == 2:
        start = datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(days=1)
        end = datetime(now.year, now.month, now.day, 0, 0, 0)
    elif period == 3:
        start = datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(weeks=1)
        end = datetime(now.year, now.month, now.day, 0, 0, 0)
    elif period == 4:
        start = datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(
            days=calendar.monthrange(now.year, now.month)[1])
        end = datetime(now.year, now.month, now.day, 0, 0, 0)
    else:
        start, end = None, None

    profit = await Database.MainBot.get_profit(shop_id, start, end)
    sales = await Database.MainBot.get_sales(shop_id, start, end)
    users = await Database.MainBot.get_users_shop(shop_id, start, end)

    await callback.message.delete()
    return await callback.message.answer(text=texts['statistics_text'].format(username=shop.username,
                                                                              profit=profit,
                                                                              sales=sales,
                                                                              users=users),
                                         reply_markup=await InlineKeyboardMain.statistics(shop_id, period))
