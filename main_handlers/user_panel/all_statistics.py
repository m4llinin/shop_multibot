import calendar
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery

from utils import load_texts
from keyboards import InlineKeyboardMain

from config.config import TZ
from database.commands import Database


async def all_statistics(callback: CallbackQuery):
    texts = await load_texts()
    period = int(callback.data.split("_")[1])

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

    user = await Database.MainBot.get_user(callback.message.chat.id)

    profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in user.shops])
    sales = sum([await Database.MainBot.get_sales(shop, start, end) for shop in user.shops])
    users = sum([await Database.MainBot.get_users_shop(shop, start, end) for shop in user.shops])

    await callback.message.delete()
    return await callback.message.answer(text=texts['allStatistics_text'].format(profit=profit,
                                                                                 sales=sales,
                                                                                 users=users),
                                         reply_markup=await InlineKeyboardMain.all_statistics(period))
