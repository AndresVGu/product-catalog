from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.models.base import Base, TimestampMixin

class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    brand: Mapped[str | None] = mapped_column(
        String(100)
    )

    sku: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        index=True
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    product_stores = relationship("ProductStore", back_populates="product")

  
