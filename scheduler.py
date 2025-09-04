import os
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
import logging

from database.utils import db_get_last_order_info

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "yummy_db")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", 5432)

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BOT_TOKEN = os.getenv("TOKEN")
MANAGER_ID = int(os.getenv("MANAGER_ID", "0"))

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/reminders.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)


async def remind_manager(cart_id: int, manager_id: int):
    bot = Bot(token=BOT_TOKEN)

    order_info = db_get_last_order_info(cart_id)
    if not order_info:
        logger.error(f"Заказ с ID {cart_id} не найден.")
        await bot.session.close()
        return

    text = (
        f"Время заказа: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"Корзина : {cart_id} \n"
        f"Клиент: {order_info['username']} \n"
        f"Сумма: {order_info['total_price']:.2f} BYN \n"
        f"Телефон: {order_info['phone']}"
    )
    logger.info(f"Отправка сообщения менеджеру... {text}")

    await bot.send_message(manager_id, text)
    await bot.session.close()
    logger.info(f"Напоминание  отправлено (order_id={cart_id})")


def schedule_reminder(cart_id: int):
    run_date = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(
        remind_manager,
        "date",
        run_date=run_date,
        args=[cart_id, MANAGER_ID],
        id=f"reminder_{cart_id}",
        replace_existing=True
    )
    logger.info(f"Задача для заказа {cart_id} запланирована на {run_date}")


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("Планировщик запущен")
