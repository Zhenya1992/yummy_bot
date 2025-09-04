from database.utils import db_get_final_cart_items


def text_for_caption(name, description, price):
    """Текст для подписи изображения."""
    return (
        f"{name}\n"
        f"Описание: {description}\n"
        f"Стоимость: {price:.2f} BYN"
    )


def counting_products_from_cart(chat_id, user_text):
    """"Функция подсчета количества товаров в корзине"""

    products = db_get_final_cart_items(chat_id)

    if products:
        text = f'<b>{user_text}</b>\n\n'
        total_products = total_price = count = 0
        for name, quantity, price, cart_id in products:
            count += 1
            total_products += quantity
            total_price += price
            text += f'<b>{count}. {name}</b>\n<b>Количество:</b> {quantity}\n<b>Стоимость:</b> {price}BYN.\n\n'
        text += (f'<b>Общее количество продуктов:</b> {total_products}\n<b>Общая стоимость :</b> '
                 f'{total_price}BYN.')
        context = (count, text, total_price, cart_id)
        return context


def get_cart_text(cart_items):
    """Генерация текста для корзины."""

    if not cart_items:
        return (
            "Ваша корзина пуста.\n"
            "Добавьте товары в корзину с помощью команды /add"
        )
    text = 'Корзина:\n\n'
    total = 0
    for item in cart_items:
        subtotal = float(item.finally_price)
        total += subtotal
        text += f'{item.product_name} - {item.quantity} шт. - {subtotal:.2f} BYN\n'
    text += f'\n💰 Общая сумма: {total:.2f} BYN\n\n'
    return text
