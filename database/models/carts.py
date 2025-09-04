from sqlalchemy import ForeignKey, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from .users import Users


class Carts(Base):
    """Класс предварительной корзины"""

    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(5, 2), default=0)
    products: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user_cart: Mapped['Users'] = relationship(back_populates='carts')
    finally_id: Mapped[int] = relationship('FinallyCarts', back_populates='user_cart')

    def __str__(self):
        return str(self.id)


class FinallyCarts(Base):
    """Класс корзины с заказом на оплату"""

    __tablename__ = 'finally_carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    finally_price: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    quantity: Mapped[int]

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    user_cart: Mapped[Carts] = relationship(back_populates='finally_id')

    __table_args__ = ({
        "sqlite_autoincrement": True
    },)

    def __str__(self):
        return str(self.id)