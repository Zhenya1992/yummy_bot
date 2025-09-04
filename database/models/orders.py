from sqlalchemy import DECIMAL, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Orders(Base):
    """Класс для хранения историй"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_name: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int]
    final_price: Mapped[DECIMAL] = mapped_column(DECIMAL(6, 2))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.product_name} : {self.quantity} : {self.final_price}"
