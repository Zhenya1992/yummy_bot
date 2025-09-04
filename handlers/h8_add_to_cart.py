from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery

from database.utils import db_get_user_cart, db_upsert_to_finally_cart
from handlers.h5_navigation import return_to_category_menu

router = Router()

@router.callback_query(F.data == "Положить в корзину")
async def add_to_cart(callback: CallbackQuery, bot: Bot):
    """Функция добавления в корзину"""

    chat_id = callback.from_user.id
    message = callback.message
    caption = message.caption

    if not caption:
        await bot.send_message(chat_id=chat_id, text="Товар не найден!")
        return

    product_name = caption.split("\n")[0]
    cart = db_get_user_cart(chat_id)

    if not cart:
        await bot.send_message(chat_id=chat_id, text="Выберите товар!")
        return

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    result = db_upsert_to_finally_cart(
        cart_id = cart.id,
        product_name=product_name,
        total_products=cart.products,
        total_price=cart.total_price,
    )

    match result:
        case "Добавлено":
            await bot.send_message(chat_id=chat_id, text= "Добавлено в корзину!")
        case "Обновлено":
            await bot.send_message(chat_id=chat_id, text= "Обновлено!")
        case "Ошибка":
            await bot.send_message(chat_id=chat_id, text= "Ошибка!")

    await return_to_category_menu(message, bot)