from pydantic import (
    BaseModel,
    field_serializer,
    field_validator,
)
from decimal import Decimal

from core.schemas.package_type import PackageTypeBase


class PackageId(BaseModel):
    id: int


class PackageAssign(BaseModel):
    delivery_service_id: int


class PackageBase(BaseModel):
    name: str
    weight: Decimal
    content_cost: Decimal

    class Config:
        json_encoders = {Decimal: lambda v: str(v)}


class PackageCreate(PackageBase):
    type_id: int


class PackageRead(PackageBase):
    delivery_cost: str
    type: PackageTypeBase
    delivery_service_id: str
    id: int

    @field_validator("delivery_cost", mode="before")
    def handle_delivery_cost(cls, value):
        return "Не рассчитано" if value is None else str(value)

    @field_validator("delivery_service_id", mode="before")
    def handle_delivery_service_id(cls, value):
        return "ТК не определена" if value is None else str(value)

    @field_serializer("type")
    def serialize_type(self, value: PackageTypeBase) -> str:
        return value.name
