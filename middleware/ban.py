from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database.commands import Database


class BlockedUserMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = await Database.MainBot.get_user(event.chat.id) or await Database.ShopBot.get_user(event.chat.id)
        if user and user.is_ban:
            return
        return await handler(event, data)


class BlockedUserCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user = await Database.MainBot.get_user(event.message.chat.id) or await Database.ShopBot.get_user(
            event.message.chat.id)
        if user and user.is_ban:
            return
        return await handler(event, data)
