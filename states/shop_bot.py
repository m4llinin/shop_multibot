from aiogram.fsm.state import State, StatesGroup


class UpdateBalance(StatesGroup):
    amount = State()


class AddQuery(StatesGroup):
    text = State()
