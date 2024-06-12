from aiogram.fsm.state import State, StatesGroup


class AddShop(StatesGroup):
    token = State()


class AddCategory(StatesGroup):
    name = State()
    description = State()


class AddSubcategory(StatesGroup):
    name = State()
    description = State()


class AddGoods(StatesGroup):
    name = State()
    description = State()
    price = State()
    count = State()
    product = State()


class EditCount(StatesGroup):
    amount = State()
