from aiogram import Router, F
from aiogram.types import Message

from database.utils import db_create_user_cart, db_register_user, db_update_user
from keyboards.reply_kb import get_main_menu
from log_actions import log_phone_number
router = Router()

@router.message(F.contact)
async def handle_update_user(message: Message):
    """Обновление юзеров"""

    chat_id = message.chat.id
    full_name = message.from_user.full_name
    phone = message.contact.phone_number

    db_update_user(chat_id, phone=phone)

    log_phone_number(username=full_name, phone_number=phone)
    db_create_user_cart(chat_id)

    await message.answer("Вы успешно зарегистрированы!")
    await show_main_menu(message)

async def show_main_menu(message: Message):
    """Показ главного меню"""

    await message.answer(
        text='Сделайте свой выбор',
        reply_markup=get_main_menu()
    )