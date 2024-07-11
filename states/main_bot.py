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
    name_on_cart = State()
    Amount = State()


class SubmitApp(StatesGroup):
    source = State()
    experience = State()
    platform = State()


class AddMail(StatesGroup):
    text = State()
    date = State()
    button = State()


class AddAllMail(StatesGroup):
    text = State()
    date = State()
    button = State()


class AddAdminMail(StatesGroup):
    text = State()
    date = State()
    button = State()


class LinkChannelAdmin(StatesGroup):
    channel = State()


class ChangeStatus(StatesGroup):
    user = State()


class Statistics(StatesGroup):
    users = State()
    shops = State()
    allPeriod = State()
    period = State()
    shop_period = State()


class Recover(StatesGroup):
    code = State()


class SupportSolution(StatesGroup):
    text = State()


class Offer(StatesGroup):
    text = State()


class AddInfobase(StatesGroup):
    question = State()
    url = State()
