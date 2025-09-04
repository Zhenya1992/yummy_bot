from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from database.utils import db_register_user
from handlers.h2_get_contact import show_main_menu
from keyboards.reply_kb import phone_button, first_button
from log_actions import log_register_user

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    """Реакция на команду /start"""

    photo = FSInputFile('media/greet.jpg')
    await message.answer_photo(
        photo=photo,
        caption=f'Привет, <i>{message.from_user.full_name}</i>\nДля работы с ботом нажмите на кнопку 👇',
        parse_mode='HTML',
        reply_markup=first_button(),
    )


@router.message(F.text == "Добро пожаловать! 👋")
async def handler_start_button(message: Message):
    await register_user(message)


async def register_user(message: Message):
    """Регистрация пользователя"""
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    log_register_user(username=full_name, user_id=chat_id)

    if db_register_user(full_name, chat_id):

        await message.answer(
            'Вы зарегистрированы! 👍'
        )
        await show_main_menu(message)
    else:
        await message.answer(text='Для работы с ботом, предоставьте номер для связи. ',
                             reply_markup=phone_button()
                             )
