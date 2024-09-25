__all__ = ['register_handlers_user_panel']

from aiogram import Router, F

from .add_new_shop import add_new_shop, new_shop

from states.main_bot import AddShop, WithdrawFunds, SubmitApp, AddAllMail, Recover, Offer
from .my_shops import shops_router
from .all_statistics import all_statistics
from .withdraw_funds import (cart_rf, payments, amount, successful_payments, bad_payments,
                             choose_payment_to_withdraw, name)
from .subpartner import (subpartner, submit_app, get_source, get_platform, get_experience, successful_request,
                         bad_request)
from .all_mailing import (all_mailing_list, all_change_page, all_view_adding_mail, all_add_mail, all_get_text_photo,
                          all_add_date, all_get_date, all_add_btn, all_get_btn, all_save_mail, all_view_profile_mail,
                          all_view_mail, all_delete_mail, edit_mail_photo, edit_mail_text, get_edit_mail_text,
                          get_edit_mail_photo)
from .recover import (recover_code, recover, recover_account, get_code, new_recover_code)
from .ppu import ppu, offer, get_offer


def register_handlers_user_panel(router: Router, ):
    router.callback_query.register(add_new_shop, F.data == "create_shop")
    router.message.register(new_shop, F.text, AddShop.token)

    router.callback_query.register(all_statistics, lambda x: x.data.startswith("allStatistics_"))

    router.callback_query.register(choose_payment_to_withdraw, F.data == "withdraw_funds")
    router.callback_query.register(cart_rf, F.data == "cart_rf")
    router.message.register(payments, F.text, WithdrawFunds.payment)
    router.message.register(name, F.text, WithdrawFunds.name_on_cart)
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

    router.callback_query.register(all_mailing_list, F.data == "all_mailing_list")
    router.callback_query.register(all_add_mail, F.data == "add_all_mail")
    router.message.register(all_get_text_photo, F.text, AddAllMail.text)
    router.message.register(all_get_text_photo, F.photo, AddAllMail.text)
    router.callback_query.register(all_view_adding_mail, F.data == "all_view_adding_mail")
    router.callback_query.register(all_add_date, F.data == "all_date")
    router.message.register(all_get_date, F.text, AddAllMail.date)
    router.callback_query.register(all_add_btn, F.data == "all_add_btn")
    router.message.register(all_get_btn, F.text, AddAllMail.button)
    router.callback_query.register(all_save_mail, F.data == "all_save_btn")

    router.callback_query.register(all_change_page,
                                   lambda x: x.data == "back_page_all_mail" or x.data == "next_page_all_mail")
    router.callback_query.register(all_view_profile_mail, lambda x: x.data.startswith("all_mail_"))
    router.callback_query.register(all_view_mail, F.data == "all_view_mail")
    router.callback_query.register(all_delete_mail, F.data == "all_delete_mail")
    shops_router.callback_query.register(edit_mail_photo, F.data == f"edit_all_mail_photo")
    shops_router.callback_query.register(edit_mail_text, F.data == f"edit_all_mail_text")
    shops_router.message.register(get_edit_mail_text, F.text, AddAllMail.edit_text)
    shops_router.message.register(get_edit_mail_photo, F.photo, AddAllMail.edit_photo)

    router.callback_query.register(recover, F.data == "recover")
    router.callback_query.register(recover_code, F.data == "recover_code")
    router.callback_query.register(new_recover_code, F.data == "new_recover_code")
    router.callback_query.register(recover_account, F.data == "recover_account")
    router.message.register(get_code, F.text, Recover.code)

    router.callback_query.register(ppu, F.data == "ppu")
    router.callback_query.register(offer, F.data == "offer")
    router.message.register(get_offer, F.text, Offer.text)

    router.include_router(shops_router)
