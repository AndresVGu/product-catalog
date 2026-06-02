from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base, TimestampMixin

class TrackingRule(Base, TimestampMixin):
    __tablename__ = "tracking_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"),
        index=True
    )

    search_query: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    category_hint: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    active: Mapped[bool] = mapped_column(
        nullable=True
    )

    store = relationship("Store")