from sqlalchemy import update, select, join, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from database.base import engine
from database.models import Users, Carts, Categories, FinallyCarts, Products, Orders


def get_session():
    """Функция получения сессии"""

    return Session(engine)


def db_register_user(full_name, chat_id):
    try:
        with get_session() as session:
            query = Users(name=full_name, telegram=chat_id)
            session.add(query)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_update_user(chat_id, phone: str):
    """Обновление данных юзера"""

    with get_session() as session:
        print(f"Обновляем {chat_id, phone}")
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id):
    """Создание корзины юзера в базе данных"""

    with get_session() as session:
        try:
            subquery = session.scalar(select(Users).where(Users.telegram == chat_id))
            query = Carts(user_id=subquery.id)
            session.add(query)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
        except AttributeError:
            session.rollback()


def db_get_all_categories():
    """Функция для получения всех категорий"""

    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """Получение итоговой цены"""

    with get_session() as session:
        query = select(func.sum(FinallyCarts.finally_price)).select_from(
            join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)).join(Users, Users.id == Carts.user_id).where(
            Users.telegram == chat_id)
        return session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id, limit=5):
    """Получение 5 последних заказов пользователя"""

    with get_session() as session:
        query = (
            select(Orders).
            join(Carts, Orders.cart_id == Carts.id).
            join(Users, Users.id == Carts.user_id).
            where(Users.telegram == chat_id).
            order_by(Orders.id.desc()).
            limit(limit)
        )
        return session.scalars(query).all()


def db_get_products_from_category(category_id):
    """Получение товаров из категории"""

    with get_session() as session:
        query = (
            select(Products).where(Products.category_id == category_id)
        )
    return session.scalars(query)


def db_get_product_by_id(product_id):
    """Получение продукта по его ID"""

    with get_session() as session:
        query = (
            select(Products).where(Products.id == product_id)
        )
        return session.scalar(query)


def db_get_product_by_name(product_name):
    """Функция получения продукта по его имени"""

    with get_session() as session:
        query = (
            select(Products).where(Products.product_name == product_name)
        )
        return session.scalar(query)


def db_get_user_cart(chat_id):
    """Функция получения корзины пользователя по ID"""

    with get_session() as session:
        query = (
            select(Carts).join(Users).where(Users.telegram == chat_id)
        )
        return session.scalar(query)


def db_update_to_cart(price, cart_id, quantity=1):
    """Функция обновления корзины пользователя"""

    with get_session() as session:
        query = (
            update(Carts).where(Carts.id == cart_id).values(total_price=price, products=quantity)
        )
        session.execute(query)
        session.commit()


def db_upsert_to_finally_cart(cart_id, product_name, total_price, total_products):
    """Добавление и обновление товаров в итоговой корзине пользователя"""

    with get_session() as session:
        try:
            item = (
                session.query(FinallyCarts).filter_by(cart_id=cart_id, product_name=product_name)
                .first()
            )
            if item:
                item.quantity = total_products
                item.finally_price = total_price
                session.commit()
                return "Обновлено"

            new_item = FinallyCarts(
                cart_id=cart_id,
                product_name=product_name,
                quantity=total_products,
                finally_price=total_price,
            )

            session.add(new_item)
            session.commit()
            return "Добавлено"

        except Exception as e:
            print(e, "Ошибка при добавлении в итоговую корзину")
            return "Ошибка"


def db_get_cart_items(chat_id: int):
    """Получение товаров из корзины пользователя"""

    with get_session() as session:
        query = (
            select(FinallyCarts)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Users.id == Carts.user_id)
            .where(Users.telegram == chat_id)
        )
        return session.scalars(query).all()


def db_get_final_cart_items(chat_id):
    """"Получение товаров из итоговой корзины пользователя"""

    with get_session() as session:
        query = (
            select(FinallyCarts.product_name,
                   FinallyCarts.quantity,
                   FinallyCarts.finally_price,
                   FinallyCarts.cart_id).
            join(Carts).join(Users).
            where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchall()


def db_get_user_phone(chat_id):
    """Функция получения телефона пользователя"""

    with get_session() as session:
        query = (
            select(Users.phone).where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchone()[0]


def db_get_products_for_delete(chat_id: int):
    """Получение товаров для удаления из корзины"""

    with get_session() as session:
        query = (
            select(FinallyCarts.id, FinallyCarts.product_name)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchall()


def db_increase_product_quantity(finally_cart_id: int):
    """Функция увеличения количества товара в корзине"""

    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity += 1
        item.finally_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_decrease_product_quantity(finally_cart_id: int):
    """Функция уменьшения количества товара в корзине"""

    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity -= 1

        if item.quantity <= 0:
            session.delete(item)
        else:
            item.finally_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_clear_finally_cart(chat_id):
    """Функция очистки итоговой корзины"""

    cart = db_get_user_cart(chat_id)
    if not cart:
        return

    with get_session() as session:
        query = delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id)

        session.execute(query)
        session.commit()


def db_save_order_history(chat_id):
    """Функция сохранения истории заказов"""

    cart = db_get_user_cart(chat_id)
    if not cart:
        return

    with get_session() as session:
        final_items = session.query(FinallyCarts).filter_by(cart_id=cart.id).all()

        for item in final_items:
            session.add(
                Orders(
                    cart_id=cart.id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    final_price=item.finally_price,
                ))

        session.commit()


def db_delete_user_by_telegram_id(chat_id):
    """Функция удаления пользователя по ID"""

    with get_session() as session:
        user = session.scalar(
            select(Users).where(Users.telegram == chat_id)
        )
        if not user:
            return False

        cart = session.scalar(
            select(Carts).where(Carts.user_id == user.id)
        )

        if cart:
            session.execute(delete(Orders).where(Orders.cart_id == cart.id))
            session.execute(delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id))
            session.execute(delete(Carts).where(Carts.id == cart.id))

        session.execute(delete(Users).where(Users.telegram == chat_id))
        session.commit()

        return True


# def db_get_order_info(cart_id):
#     """Функция для получения данных для напоминания менеджеру"""
#
#     from sqlalchemy import func
#     with get_session() as session:
#         total = session.query(func.sum(Orders.final_price)) \
#                     .filter(Orders.cart_id == cart_id).scalar() or 0.0
#
#         user = session.query(Users) \
#             .join(Carts, Users.id == Carts.user_id) \
#             .filter(Carts.id == cart_id).first()
#
#         return {
#             "username": user.name if user else 'Отсутствует',
#             "phone": user.phone if user else 'Отсутствует',
#             "total_price": float(total)
#         }

def db_get_last_order_info(cart_id: int):
    """Функция для получения данных о последнем заказе"""

    with (get_session() as session):
        orders = session.query(Orders) \
        .filter(Orders.cart_id==cart_id) \
        .order_by(Orders.created_at.desc()).all()
        if not orders:
            return None

        last_order_time = orders[0].created_at
        last_order_items = [order for order in orders if order.created_at == last_order_time]

        user = session.query(Users) \
        .join(Carts, Users.id == Carts.user_id) \
        .filter(Carts.id == cart_id).first()

        items = []
        total_price = 0
        for item in last_order_items:
            item_total = float(item.final_price) * item.quantity
            items.append({
                'name': item.product_name,
                'quantity': item.quantity,
                'price': float(item.final_price),
                'total': item_total
            })
            total_price += item_total

        return {
            "username": user.name if user else "Неизвестно",
            "phone": user.phone if user else "-",
            "total_price": total_price,
            "items": items
        }