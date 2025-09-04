from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from handlers.h3_make_order import make_order

router = Router()

@router.message(F.text == "⬅️ Назад")
async def return_to_category_menu(message: Message, bot: Bot):
    """Обработчик кнопки назад и удаление предыдущего сообщения"""

    chat_id = message.chat.id
    message_id = message.message_id
    try:
        await bot.delete_message(chat_id, message_id - 1)
    except TelegramBadRequest:
        pass

    await make_order(message, bot)
