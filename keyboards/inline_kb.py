from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import Products
from database.utils import db_get_all_categories, db_get_finally_price, db_get_products_from_category
from config import MANAGER_ID


def show_category_menu(chat_id):
    """Кнопка показа категорий товара"""

    categories = db_get_all_categories()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    [builder.button(text=category.category_name, callback_data=f"category_{category.id}") for category in categories]

    builder.button(
        text=f"Сумма заказа ({total_price if total_price else '0'}руб.)",
        callback_data="Сумма заказа",
    )

    builder.adjust(1, 2)
    return builder.as_markup()


def show_product_by_category(category_id):
    """Кнопка показа товаров по категории"""

    products = db_get_products_from_category(category_id)

    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name, callback_data=f"product_{product.id}") for product in products]

    builder.adjust(1, 2)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="Назад"))

    return builder.as_markup()


def cart_quantity_controller(quantity=1):
    """Кнопка контроллера количества товара"""

    builder = InlineKeyboardBuilder()
    builder.button(text="➕", callback_data="action +")
    builder.button(text=str(quantity), callback_data="quantity")
    builder.button(text="➖", callback_data="action -")
    builder.button(text="🧺 Добавить в корзину", callback_data="Положить в корзину")

    builder.adjust(3, 1)
    return builder.as_markup()


def cart_action_controller():
    """Кнопка контроллера корзины"""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Оформить заказ", callback_data="Confirm_order"),
        InlineKeyboardButton(text="Убрать", callback_data="remove"),
        InlineKeyboardButton(text="Добавить", callback_data="add"),
    )
    builder.adjust(1, 2)
    return builder.as_markup()


def show_settings_menu():
    """Кнопка показа настроек"""

    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить аккаунт', callback_data='delete_account')
    builder.button(text='Открыть профиль Instagram', url='https://www.instagram.com/golenko.cake27/')
    if MANAGER_ID:
        builder.button(
            text='Связаться с менеджером 📲',
            url=f'tg://user?id={MANAGER_ID}',
        )
    builder.button(text='Назад', callback_data='get_main_menu')
    builder.adjust(2, 1)
    return builder.as_markup()

def delete_account_kb():
    """Кнопка подтверждения удаления аккаунта"""

    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data='delete_account_confirm')
    builder.button(text='Нет', callback_data='show_settings')
    builder.adjust(2)
    return builder.as_markup()