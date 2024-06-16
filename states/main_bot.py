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


class AddUsersDB(StatesGroup):
    db = State()


class LinkChannel(StatesGroup):
    channel = State()


class EditToken(StatesGroup):
    token = State()


class WithdrawFunds(StatesGroup):
    payment = State()
    Amount = State()


class SubmitApp(StatesGroup):
    source = State()
    experience = State()
    platform = State()
