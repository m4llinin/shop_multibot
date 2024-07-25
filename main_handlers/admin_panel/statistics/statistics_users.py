import csv
import os
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from config.config import TZ
from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database

from states.main_bot import Statistics


async def statistics_users(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    texts = await load_texts()
    partners, subpartners = await Database.MainBot.statistics_users()
    shops = await Database.MainBot.get_all_shops()

    await state.set_state(Statistics.users)
    await callback.message.delete()
    await callback.message.answer(text=texts['statistics_users_text'].format(partners, subpartners, len(shops)),
                                  reply_markup=await InlineKeyboardMain.download_users())


async def download_users(callback: CallbackQuery):
    users = await Database.MainBot.get_all_users()
    now = datetime.now(TZ)
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = datetime(now.year, now.month, now.day, 23, 59, 59)

    with open("users_statistics.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["username", "Кол-во афилиатов", "Кол-во подключенных магазинов", "Линки магазинов",
                             "Кол-во продаж за сегодня"])
        for user in users:
            shops = await Database.MainBot.get_shops(user.id)
            subpartners = await Database.MainBot.get_subpartners(user.id)
            profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in user.shops])
            csv_writer.writerow(
                [user.username, len(subpartners), len(shops), " ".join([shop.username for shop in shops]), profit])
    await callback.message.answer_document(
        document=FSInputFile("users_statistics.csv", filename="users_statistics.csv"))
    return os.remove("users_statistics.csv")


async def get_username(message: Message, state: FSMContext):
    texts = await load_texts()
    username = message.text
    if username[0] == "@":
        username = message.text[1:]

    user = await Database.MainBot.get_user(username)
    if not user:
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))

    shops = await Database.MainBot.get_shops(user.id)
    shops_links = ""
    for shop in shops:
        shops_links += f"{shop.name}\n@{shop.username}\n\n"

    await state.set_state(None)
    await message.answer(text=texts['shops_links'].format(user.username, len(shops)) + shops_links,
                         reply_markup=await InlineKeyboardMain.back("admin_statistics_users"))
