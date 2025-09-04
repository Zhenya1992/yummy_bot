from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Users(Base):
    """Класс пользователей"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    carts: Mapped[int] = relationship('Carts', back_populates='user_cart')

    def __str__(self):
        return self.name
