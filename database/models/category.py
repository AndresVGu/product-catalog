from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from database.models.product import Product

class Category(Base, TimestampMixin):
    __tablename__= "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )