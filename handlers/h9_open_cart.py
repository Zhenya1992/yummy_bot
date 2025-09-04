from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from database.utils import db_get_cart_items
from keyboards.inline_kb import cart_action_controller

router = Router()


@router.message(F.text == 'Корзина 🧺')
async def handle_cart(message: Message):
    """Обработчик сообщения с текстом 'Корзина 🧺'"""

    await show_cart(chat_id=message.chat.id, send_fn=message.answer)


@router.callback_query(F.data == 'Сумма заказа')
async def open_cart(callback: CallbackQuery):
    """Обработчик inline-кнопки на 'Сумму заказа'"""

    await show_cart(chat_id=callback.from_user.id, send_fn=callback.message.answer)
    await callback.answer()


async def show_cart(chat_id: int, send_fn):
    """Функция показа содержимого корзины"""

    cart_items = db_get_cart_items(chat_id)
    if not cart_items:
        await send_fn(
            'Ваша корзина пуста! 🧺'
        )
        return

    text = '🧺 Содержимое корзины:\n\n'
    total = 0
    for item in cart_items:
        subtotal = float(item.finally_price)
        total += subtotal
        text += f'{item.product_name} - {item.quantity} шт. - {subtotal:.2f} BYN\n'
    text += f'\n💰 Общая сумма: {total:.2f} BYN\n\n'

    await send_fn(text, reply_markup=cart_action_controller())
