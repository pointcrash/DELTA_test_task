from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


if TYPE_CHECKING:
    from .package_type import PackageType


class Package(IntIdPkMixin, Base):
    session_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    content_cost: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    delivery_cost: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=True)
    delivery_service_id: Mapped[int] = mapped_column(nullable=True)

    type_id: Mapped[int] = mapped_column(
        ForeignKey("package_types.id"),
        nullable=False,
    )
    type: Mapped["PackageType"] = relationship(back_populates="packages")
