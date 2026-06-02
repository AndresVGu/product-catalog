from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base, TimestampMixin


class Store(Base, TimestampMixin):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index = True
    )

    country: Mapped[str] = mapped_column(
        String(2)
    )

    website: Mapped[str | None] = mapped_column(

        String(255)
    )

    product_stores = relationship("ProductStore", back_populates="store")

 
