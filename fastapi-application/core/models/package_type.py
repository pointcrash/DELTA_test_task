from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class PackageType(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
