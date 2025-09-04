from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from handlers.h2_get_contact import show_main_menu
from keyboards.inline_kb import show_product_by_category, show_category_menu

router = Router()

@router.callback_query(F.data.regexp(r'^category_(\d+)$'))
async def show_product_buttons(callback: CallbackQuery):
    """Обработчик для отображения продуктов в категории"""

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    category_id = int(callback.data.split('_')[-1])

    try:
        await callback.bot.edit_message_text(
            text=f"Выберите продукт:",
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=show_product_by_category(category_id)
        )
    except TelegramBadRequest:
        await callback.answer("Не найдена выбранная категория")


@router.callback_query(F.data == 'Назад')
async def back_to_categories(callback: CallbackQuery):
    """Обработчик для возвращения назад в категорию"""

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await callback.bot.edit_message_text(
        text=f"Выберите категорию:",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=show_category_menu(chat_id)
    )