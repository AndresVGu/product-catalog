from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base, TimestampMixin

class ProductStore(Base, TimestampMixin):
    __tablename__ = "product_stores"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True
    )

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"),
        index=True
    )

    store_sku: Mapped[str | None] = mapped_column(
        String(100),
        index=True
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    product = relationship("Product", back_populates="product_store")
    store = relationship("Store", back_populates="product_store")
    prices = relationship("Price", back_populates="product_store")