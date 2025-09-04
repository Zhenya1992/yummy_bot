from log_settings import logger


def log_register_user(username: str, user_id, phone_number: str | None = None):
    """"Добавляет в лог регистрацию пользователя"""

    if phone_number:
        logger.info(f"Пользователь {username} зарегистрировался с номером телефона {phone_number} и id={user_id}")
    else:
        logger.info(f"Пользователь {username} c номером телефона и id={user_id} не предоставил")


def log_phone_number(username, phone_number):
    """Добавляет в лог номер телефона"""

    logger.info(f"Пользователь {username} добавил номер телефона {phone_number}")


def log_delete_user(username, user_id):
    """Добавляет в лог удаление пользователя"""

    logger.info(f"Пользователь {username} c id={user_id} удален")