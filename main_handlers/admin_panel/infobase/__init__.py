__all__ = ['router']

import asyncio

from aiogram import Router, F

from states.main_bot import AddInfobase
from utils import load_infobase

from .edit_infobase import edit_infobase
from .add import add_infobase, get_url, get_question
from .delete import delete_infobase, delete_key

router = Router()

router.callback_query.register(edit_infobase, F.data == "edit_infobase")

router.callback_query.register(add_infobase, F.data == "add_infobase")
router.message.register(get_question, F.text, AddInfobase.question)
router.message.register(get_url, F.text, AddInfobase.url)

router.callback_query.register(delete_infobase, F.data == "delete_infobase")
router.callback_query.register(delete_key, lambda x: x.data in asyncio.run(load_infobase()))
