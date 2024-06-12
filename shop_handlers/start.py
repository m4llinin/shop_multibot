from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from keyboards.shop.inline import InlineKeyboardShop
from utils import load_texts, Cart
from keyboards import RelpyKeyboardShop
from database.commands import Database


async def start(message: Message, state: FSMContext):
    texts = await load_texts()
    user_id = message.chat.id
    split_text = message.text.split(' ')
    shop = await Database.MainBot.get_shop(message.bot.id)

    referral_id = None
    if len(split_text) == 2 and not ("good" in split_text[1]):
        if int(split_text[1]) != message.chat.id:
            referral_id = int(split_text[1])

    if shop.channel:
        status_channel = await message.bot.get_chat_member(chat_id=shop.channel, user_id=user_id)
        if status_channel.status == "left":
            await state.update_data(referral_id=referral_id)
            return message.answer(photo=FSInputFile("./photos/hello_shop_bot.jpeg"),
                                  caption=texts['subscribe_channel'],
                                  reply_markup=await InlineKeyboardShop.subscribe(shop.channel),
                                  parse_mode=ParseMode.HTML)

    if len(split_text) == 2 and "good" in split_text[1]:
        good_id = int(split_text[1].split("_")[1])
        good = await Database.ShopBot.get_good_by_id(good_id)
        extra_charge = (shop.extra_charge / 100) + 1 if shop.extra_charge != 0 else 1
        cart = Cart(good=good, extra_charge=extra_charge, shop_name=shop.username)
        await Database.ShopBot.insert_user(user_id=user_id)
        return await message.answer(text=texts['good'].format(good_name=good.name,
                                                              good_description=good.description,
                                                              price=good.price * extra_charge),
                                    reply_markup=await InlineKeyboardShop.good_kb(cart,
                                                                                  f"subcategory_{good.subcategory_id}" if
                                                                                  good.subcategory_id != 0 else
                                                                                  f"category_{good.category_id}"),
                                    parse_mode=ParseMode.HTML)

    await Database.ShopBot.insert_user(user_id=user_id, referral_id=referral_id)
    return await message.answer_photo(photo=FSInputFile("./photos/hello_shop_bot.jpeg"), caption=texts['start_shop'],
                                      reply_markup=await RelpyKeyboardShop.start_kb(),
                                      parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def start_clb(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user_id = callback.message.chat.id
    shop = await Database.MainBot.get_shop(callback.bot.id)
    referral_id = (await state.get_data()).get('referral_id', None)

    await callback.message.delete()

    if shop.channel:
        status_channel = await callback.message.bot.get_chat_member(chat_id=shop.channel, user_id=user_id)
        if status_channel.status == "left":
            return callback.message.answer_photo(photo=FSInputFile("./photos/hello_shop_bot.jpeg"),
                                                 caption=texts['subscribe_channel'],
                                                 reply_markup=await InlineKeyboardShop.subscribe(shop.channel),
                                                 parse_mode=ParseMode.HTML)

    await Database.ShopBot.insert_user(user_id=user_id, referral_id=referral_id)
    return await callback.message.answer_photo(photo=FSInputFile("./photos/hello_shop_bot.jpeg"),
                                               caption=texts['start_shop'],
                                               reply_markup=await RelpyKeyboardShop.start_kb(),
                                               parse_mode=ParseMode.HTML, disable_web_page_preview=True)
