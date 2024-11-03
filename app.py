import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, TokenBasedRequestHandler, setup_application
from aiohttp import web

from config.config import (BASE_URL, MAIN_BOT_PATH, main_dispatcher, multibot_dispatcher, main_bot, session,
                           OTHER_BOTS_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, schedular, client)
from shop_handlers import register_shop_handler
from main_handlers import register_main_handler

from database.commands import Database
from utils import handler_prodamus_request, handler_prodamus_update_balance

from utils import recover_mails
from middleware.ban import BlockedUserMessageMiddleware, BlockedUserCallbackMiddleware

logger = logging.getLogger(__name__)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(f"{BASE_URL}{MAIN_BOT_PATH}", drop_pending_updates=True)
    commands = [BotCommand(command="start", description="❕МЕНЮ❕"),
                BotCommand(command="privacy", description="Политика конфиденциальности")]
    await bot.set_my_commands(commands=commands)
    schedular.start()


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook()


async def on_startup_app(application: web.Application):
    await recover_mails()


async def on_shutdown_app(application: web.Application):
    logger.info("Bot was stopped")
    await client.close()
    return await session.close()


def main():
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=main_bot).register(app, path=MAIN_BOT_PATH)
    TokenBasedRequestHandler(dispatcher=multibot_dispatcher, session=session,
                             default=DefaultBotProperties(parse_mode=ParseMode.HTML)).register(app,
                                                                                               path=OTHER_BOTS_PATH)

    Database.setup(app)
    setup_application(app, main_dispatcher, bot=main_bot)
    setup_application(app, multibot_dispatcher)
    app.router.add_route("POST", "/prodamus", handler_prodamus_request)
    app.router.add_route("POST", "/prodamus/balance", handler_prodamus_update_balance)
    app.router.add_route("POST", "/cryptopay", client.get_updates)

    app.on_startup.append(on_startup_app)
    app.on_shutdown.append(on_shutdown_app)

    register_main_handler(main_dispatcher)
    register_shop_handler(multibot_dispatcher)
    main_dispatcher.message.outer_middleware(BlockedUserMessageMiddleware())
    main_dispatcher.callback_query.outer_middleware(BlockedUserCallbackMiddleware())
    multibot_dispatcher.message.outer_middleware(BlockedUserMessageMiddleware())
    multibot_dispatcher.callback_query.outer_middleware(BlockedUserCallbackMiddleware())

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    try:
        logger.info("Bot was started")
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
