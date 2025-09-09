from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_utils.message_utils import get_cart_text
from database.utils import (
    db_get_products_for_delete,
    db_increase_product_quantity,
    db_decrease_product_quantity,
    db_get_cart_items
)
from keyboards.inline_kb import cart_action_controller
from keyboards.reply_kb import back_to_main_menu

router = Router()


@router.callback_query(F.data == 'add')
async def choose_product_to_add(callback: CallbackQuery):
    """Обработчик кнопки "Добавления товаров" в корзину."""

    cart_products = db_get_products_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➕ {name}', callback_data=f'increase_{cart_id}')
    builder.button(text=" Назад", callback_data="back_to_cart_review")
    builder.adjust(1)

    await callback.message.edit_text(
        "Выберите товар для увеличения количества:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == 'remove')
async def choose_product_to_remove(callback: CallbackQuery):
    """Обработчик кнопки "Удаления товаров" из корзины."""

    cart_products = db_get_products_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➖ {name}', callback_data=f'decrease_{cart_id}')
    builder.button(text=" Назад", callback_data="back_to_cart_review")
    builder.adjust(1)

    await callback.message.edit_text(
        "Выберите товар для уменьшения количества:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    """Обработчик кнопки увеличения количества."""

    cart_id = int(callback.data.split("_")[1])
    db_increase_product_quantity(cart_id)

    user_id = callback.from_user.id
    cart_items = db_get_cart_items(user_id)
    text = get_cart_text(cart_items)

    builder = InlineKeyboardBuilder()
    builder.button(text=" Назад", callback_data="back_to_cart_review")
    builder.button(text="➕ Добавить кол-во", callback_data=f"increase_{cart_id}")
    builder.adjust(1)

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
    await callback.answer("Количество увеличено.")


@router.callback_query(F.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    """Обработчик кнопки уменьшения количества."""

    cart_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    new_quantity = db_decrease_product_quantity(cart_id)

    if new_quantity == 0:
        await callback.message.edit_text(
            " Ваш заказ пуст, сделайте его заново.",
            reply_markup=back_to_main_menu()
        )
    else:
        cart_items = db_get_cart_items(user_id)
        text = get_cart_text(cart_items)
        keyboard = cart_action_controller()
        await callback.message.edit_text(text, reply_markup=keyboard)

    await callback.answer("Количество уменьшено.")
@router.callback_query(F.data == "back_to_cart_review")
async def back_to_cart(callback: CallbackQuery):
    """Обработчик кнопки "Назад" к корзине."""

    await callback.message.edit_text("Ваша корзина:", reply_markup=cart_action_controller())
    await callback.answer()