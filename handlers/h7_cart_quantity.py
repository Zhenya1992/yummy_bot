from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from bot_utils.message_utils import text_for_caption
from database.utils import db_get_product_by_name, db_get_user_cart, db_update_to_cart
from keyboards.inline_kb import cart_quantity_controller

router = Router()


@router.callback_query(F.data.regexp(r"action [+-]"))
async def change_product_quantity(callback: CallbackQuery, bot: Bot):
    """Обработчик изменения количества товара в корзине"""

    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    action = callback.data.split()[-1]

    product_name = callback.message.caption.split('\n')[0]
    product = db_get_product_by_name(product_name)

    user_cart = db_get_user_cart(chat_id)

    if not product or not user_cart:
        await callback.answer('Ошибка! Товар или корзина не найдены')
        return

    current_quantity = user_cart.products
    new_quantity = current_quantity

    if action == '+':
        new_quantity += 1
    elif action == '-' and current_quantity > 1:
        new_quantity -= 1
    elif action == '-' and current_quantity <= 1:
        await callback.answer('Количество товара должно быть больше 1')
        return

    total_price = product.price * new_quantity
    db_update_to_cart(price=total_price, quantity=new_quantity, cart_id=user_cart.id)

    caption = text_for_caption(
        name=product.product_name,
        description=product.description,
        price=total_price,
    )

    try:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                media=FSInputFile(path=product.image),
                caption=caption,
            ),
            reply_markup=cart_quantity_controller(new_quantity)
        )
    except TelegramBadRequest:
        pass
