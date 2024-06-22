import calendar
from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import TZ
from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database

from states.main_bot import Statistics


async def statistics_shops(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    await state.set_state(Statistics.shops)
    await callback.message.delete()
    await callback.message.answer(text=texts['input_username'],
                                  reply_markup=await InlineKeyboardMain.back("admin_statistics"))


async def get_username_shops(message: Message, state: FSMContext):
    texts = await load_texts()

    username = message.text
    if username[0] == "@":
        username = message.text[1:]

    user = await Database.MainBot.get_user(username)
    if not user:
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))
    now = datetime.now(TZ)
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = datetime(now.year, now.month, now.day, 23, 59, 59)

    profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in user.shops])
    sales = sum([await Database.MainBot.get_sales(shop, start, end) for shop in user.shops])
    users = sum([await Database.MainBot.get_users_shop(shop, start, end) for shop in user.shops])

    await state.update_data(username=username)
    await state.set_state(None)
    await message.answer(text=texts['adminStatistics_text'].format(profit=profit,
                                                                   sales=sales,
                                                                   users=users,
                                                                   username=username),
                         reply_markup=await InlineKeyboardMain.admin_statistics())


async def admin_statistics_shops(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    username = (await state.get_data()).get("username")
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

    user = await Database.MainBot.get_user(username)

    profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in user.shops])
    sales = sum([await Database.MainBot.get_sales(shop, start, end) for shop in user.shops])
    users = sum([await Database.MainBot.get_users_shop(shop, start, end) for shop in user.shops])

    await callback.message.delete()
    return await callback.message.answer(text=texts['adminStatistics_text'].format(profit=profit,
                                                                                   sales=sales,
                                                                                   users=users,
                                                                                   username=username),
                                         reply_markup=await InlineKeyboardMain.admin_statistics(period))
