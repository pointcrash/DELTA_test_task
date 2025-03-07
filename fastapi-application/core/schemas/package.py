from pydantic import BaseModel, field_serializer, computed_field
from decimal import Decimal

from core.schemas.package_type import PackageTypeBase


class PackageId(BaseModel):
    id: int


class PackageBase(BaseModel):
    name: str
    weight: Decimal
    content_cost: Decimal

    class Config:
        json_encoders = {Decimal: lambda v: str(v)}


class PackageCreate(PackageBase):
    type_id: int


class PackageRead(PackageBase):
    delivery_cost: Decimal | None
    type: PackageTypeBase

    @computed_field(return_type=str)
    @property
    def delivery_cost_display(self) -> str:
        return (
            "Не рассчитано" if self.delivery_cost is None else str(self.delivery_cost)
        )

    @field_serializer("type")
    def serialize_type(self, value: PackageTypeBase) -> str:
        return value.name
