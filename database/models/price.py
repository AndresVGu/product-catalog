from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.models.base import Base, TimestampMixin
from decimal import Decimal

class Price(Base, TimestampMixin):
    __tablename__= "prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_store_id: Mapped[int] = mapped_column(
        ForeignKey("product_stores.id"),
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="CAD"
    )

    product_store = relationship("ProductStore", back_populates="prices")