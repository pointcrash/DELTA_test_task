from pydantic import BaseModel, field_serializer, computed_field, model_serializer
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
    id: int
    delivery_cost: Decimal | None
    type: PackageTypeBase
    delivery_service_id: int | None

    @field_serializer("type")
    def serialize_type(self, value: PackageTypeBase) -> str:
        return value.name
