import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import (
    h1_startup, h2_get_contact, h3_make_order, h4_categories,
    h5_navigation, h6_product_detail, h7_cart_quantity, h8_add_to_cart,
    h9_open_cart, h10_confirm_order, h11_cart_modify, h12_settings
)
from scheduler import start_scheduler
from database.initial_db import create_db
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h1_startup.router)
dp.include_router(h2_get_contact.router)
dp.include_router(h3_make_order.router)
dp.include_router(h4_categories.router)
dp.include_router(h5_navigation.router)
dp.include_router(h6_product_detail.router)
dp.include_router(h7_cart_quantity.router)
dp.include_router(h8_add_to_cart.router)
dp.include_router(h9_open_cart.router)
dp.include_router(h10_confirm_order.router)
dp.include_router(h11_cart_modify.router)
dp.include_router(h12_settings.router)

async def main():
    start_scheduler()
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
