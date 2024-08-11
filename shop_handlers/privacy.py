from aiogram.types import Message
from utils import load_texts


async def privacy(message: Message):
    texts = await load_texts()
    await message.answer(text=texts['privacy_policy'], disable_web_page_preview=True, parse_mode="HTML")
