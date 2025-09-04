from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from database.utils import db_get_last_orders
from handlers.h2_get_contact import show_main_menu
from keyboards.inline_kb import show_category_menu
from keyboards.reply_kb import back_to_main_menu

router = Router()

@router.message(F.text == "Сделать заказ 📖")
async def make_order(message: Message, bot: Bot):
    """Обработчик реакции на кнопку 'Сделать заказ 📖'"""

    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Выберите из меню", reply_markup=back_to_main_menu())
    await message.answer(text="⬇️ Категории", reply_markup=show_category_menu(chat_id))


@router.message(F.text == 'История заказов 📚')
async def order_history(message: Message):
    """Обработчик реакции на кнопку 'История заказов 📚'"""

    chat_id = message.chat.id
    orders = db_get_last_orders(chat_id)

    if not orders:
        await message.answer(text="Вы еще не делали заказов")
        return

    text = "История последних 5- заказов:\n\n"
    for order in orders:
        text += f"{order.product_name} - {order.final_price}руб. в количестве: {order.quantity}\n"
    await message.answer(text)


@router.message(F.text == 'Главное меню 🏠')
async def open_to_main_menu(message: Message, bot: Bot):
    """Обработчик реакции на кнопку 'Главное меню 🏠'"""

    chat_id = message.chat.id
    try:
        await bot.delete_message(chat_id, message_id=message.message_id - 1)
    except TelegramBadRequest:
        pass

    await show_main_menu(message)