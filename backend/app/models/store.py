from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    owner_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    subscription_plan: Mapped[str] = mapped_column(
        String(50),
        default="free"
    )