import os
import logging

import betterlogging as bl
import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()
bl.basic_colorized_config(level=logging.INFO)

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

BASE_URL = os.getenv("BASE_URL")
MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
MAIN_BOT_ID = os.getenv("MAIN_BOT_ID")
MAIN_BOT_LINK = os.getenv("MAIN_BOT_LINK")

PRODAMUS_API = os.getenv("PRODAMUS_API")
PRODAMUS_LINK = os.getenv("PRODAMUS_LINK")

WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))
MAIN_BOT_PATH = "/webhook/main"
OTHER_BOTS_PATH = "/webhook/bot/{bot_token}"

OTHER_BOTS_URL = f"{BASE_URL}{OTHER_BOTS_PATH}"

session = AiohttpSession()
main_bot = Bot(token=MAIN_BOT_TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = MemoryStorage()
main_dispatcher = Dispatcher(storage=storage)
multibot_dispatcher = Dispatcher(storage=storage)

POSTGRES_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}"

TZ = pytz.timezone(os.getenv("TZ"))
