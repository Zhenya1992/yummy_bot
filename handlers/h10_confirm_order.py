from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import MANAGER_ID

from bot_utils.message_utils import counting_products_from_cart
from database.utils import db_get_user_phone, db_clear_finally_cart, db_save_order_history
from scheduler import schedule_reminder

router = Router()


@router.callback_query(F.data == "Confirm_order")
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """Реакция на кнопку подтверждения заказа"""

    user = callback.from_user

    phone = db_get_user_phone(user.id)
    mention = f"<a href='tg://user?id={user.id}'>{user.full_name} </a>"
    user_text = f"Новый заказ от {mention}\nс номером телефона {phone}!"
    context = counting_products_from_cart(user.id, user_text)
    print(context)


    if not context:
        await callback.message.edit_text('Корзина пуста, оформление заказа невозможно!')
        await callback.answer()
        return

    if not MANAGER_ID:
        await callback.message.edit_text("Менеджер не указан!")
        await callback.answer()
        return

    count, text, total_price, cart_id = context

    await bot.send_message(MANAGER_ID, text, parse_mode="HTML")

    db_save_order_history(user.id)
    schedule_reminder(cart_id)
    db_clear_finally_cart(callback.from_user.id)

    await callback.message.edit_text("Ваш заказ принят! ✅ Ожидайте обратной связи от менеджера!\n"
                                     "Для связи с менеджером, воспользуйтесь кнопкой в настройках")
    await callback.answer("Заказ оформлен! 🎉")