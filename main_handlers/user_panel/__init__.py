__all__ = ['register_handlers_user_panel']

from aiogram import Router, F

from .add_new_shop import add_new_shop, new_shop

from states.main_bot import AddShop, WithdrawFunds, SubmitApp
from .my_shops import shops_router
from .all_statistics import all_statistics
from .withdraw_funds import withdraw_funds, payments, amount, successful_payments, bad_payments
from .subpartner import (subpartner, submit_app, get_source, get_platform, get_experience, successful_request,
                         bad_request)


def register_handlers_user_panel(router: Router):
    router.callback_query.register(add_new_shop, F.data == "create_shop")
    router.message.register(new_shop, F.text, AddShop.token)

    router.callback_query.register(all_statistics, lambda x: x.data.startswith("allStatistics_"))

    router.callback_query.register(withdraw_funds, F.data == "withdraw_funds")
    router.message.register(payments, F.text, WithdrawFunds.payment)
    router.message.register(amount, F.text, WithdrawFunds.Amount)
    router.callback_query.register(successful_payments, lambda x: x.data.startswith("successful_payments_"))
    router.callback_query.register(bad_payments, lambda x: x.data.startswith("bad_payments_"))

    router.callback_query.register(subpartner, F.data == "subpartner")
    router.callback_query.register(submit_app, F.data == "submit_app")
    router.message.register(get_source, F.text, SubmitApp.source)
    router.message.register(get_experience, F.text, SubmitApp.experience)
    router.message.register(get_platform, F.text, SubmitApp.platform)
    router.callback_query.register(successful_request, lambda x: x.data.startswith("successful_request_"))
    router.callback_query.register(bad_request, lambda x: x.data.startswith("bad_request_"))

    router.include_router(shops_router)
