import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from database.schemas.Shop import Shop
from utils import load_texts
from keyboards import InlineKeyboardMain

from states.main_bot import AddUsersDB
from database.commands import Database


async def users_db(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    await state.set_state(AddUsersDB.db)
    await callback.message.delete()
    return await callback.message.answer(text=texts['users_db'].format(shop.username),
                                         reply_markup=await InlineKeyboardMain.users_db(shop.id))


async def send_users_db(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    users = await Database.MainBot.get_users_shop_list(shop.id)

    if not users:
        return await callback.answer(text=texts['no_users'], show_alert=True)

    with open(f"{shop.id}.txt", "w") as file:
        for user in users:
            file.write(f"{user.id}\n")

    await callback.message.delete()
    await callback.message.answer_document(document=FSInputFile(f"{shop.id}.txt", "users.txt"),
                                           caption=texts['send_users_db'].format(shop.username),
                                           reply_markup=await InlineKeyboardMain.back(f"settings_{shop.id}"))
    return os.remove(f"{shop.id}.txt")


async def get_users_db(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")
    document = message.document

    if document.file_name.endswith('.txt'):
        await message.bot.download(document.file_id, f"{shop.id}.txt")

        counter = 0
        with open(f"{shop.id}.txt", 'r') as file:
            for line in file:
                try:
                    user_id = int(line)
                    await Database.ShopBot.insert_user(user_id=user_id, shop_id=shop.id)
                    counter += 1
                except ValueError:
                    pass
        os.remove(f"{shop.id}.txt")

        return await message.answer(text=texts['get_users_db'].format(counter),
                                    reply_markup=await InlineKeyboardMain.ready(f"shop_{shop.id}"))
    return await message.answer(text=texts['not_get_users_db'])
