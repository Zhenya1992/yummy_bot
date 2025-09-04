from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


def first_button():
    """Стартовая кнопка"""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Добро пожаловать! 👋')]], resize_keyboard=True)


def phone_button():
    """Кнопка для отправки номера телефона"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона 📞", request_contact=True)
    return builder.as_markup(resize_keyboard=True)


def get_main_menu():
    """Функция для получения главного меню"""

    builder = ReplyKeyboardBuilder()
    builder.button(text='Сделать заказ 📖')
    builder.button(text='Корзина 🧺')
    builder.button(text='История заказов 📚')
    builder.button(text='Настройки ⚙️')
    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def back_to_main_menu():
    """Кнопка для возврата в главное меню"""

    builder = ReplyKeyboardBuilder()
    builder.button(text='Главное меню 🏠')
    return builder.as_markup(resize_keyboard=True)


def back_arrow_button():
    """Кнопка назад"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="⬅️ Назад")
    return builder.as_markup(resize_keyboard=True)
