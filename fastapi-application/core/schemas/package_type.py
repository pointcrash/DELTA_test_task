from pydantic import BaseModel


class PackageTypeBase(BaseModel):
    name: str


class PackageTypeCreate(PackageTypeBase):
    pass


class PackageTypeUpdate(PackageTypeBase):
    pass


class PackageTypePartialUpdate(PackageTypeBase):
    name: str | None = None


class PackageTypeRead(PackageTypeBase):
    id: int
