from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


if TYPE_CHECKING:
    from .package import Package


class PackageType(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    packages: Mapped[list["Package"]] = relationship(back_populates="type")

    def __str__(self):
        return self.name
