from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import InlineKeyboardShop
from utils import load_texts, Cart


async def edit_count_cart(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    cart: Cart | None = data.get("cart", None)
    action, count, good_id = callback.data.split("_")
    count, good_id = int(count), int(good_id)

    if cart and cart.good.id == good_id:
        if action == "plus":
            if cart.count + count > cart.good.count:
                return await callback.answer(text=texts['have_not_count_good'], show_alert=True)
            cart.count += count
        else:
            if cart.count - count <= 0:
                return await callback.answer(text=texts['min_count'], show_alert=True)
            cart.count -= count

        await state.update_data(cart=cart)
        await callback.message.delete()
        return await callback.message.answer(text=texts['good'].format(good_name=cart.good.name,
                                                                       good_description=cart.good.description,
                                                                       price=cart.good.price * cart.extra_charge),
                                             reply_markup=await InlineKeyboardShop.good_kb(cart,
                                                                                           f"subcategory_{cart.good.subcategory_id}" if cart.good.subcategory_id != 0 else f"category_{cart.good.category_id}"),
                                             parse_mode=ParseMode.HTML)
    return await callback.answer(text="ERROR", show_alert=True)


async def just_count(callback: CallbackQuery):
    texts = await load_texts()
    return await callback.answer(text=texts['just_count'], show_alert=True)
