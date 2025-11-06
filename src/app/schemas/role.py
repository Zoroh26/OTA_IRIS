from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    role_name: Annotated[
        str,
        Field(min_length=2, max_length=50, examples=["Admin", "Publisher"])
    ]
    status: Annotated[
        str,
        Field(pattern=r"^(Active|Inactive)$",
              examples=["Active"], default="Active")
    ] = "Active"
    description: Annotated[
        str | None,
        Field(max_length=1000, examples=["Can manage users"], default=None)
    ] = None


class RoleCreate(RoleBase):
    model_config = ConfigDict(extra="forbid")


class RoleRead(RoleBase):
    role_id: int
    created_at: datetime
    updated_at: datetime


class RoleUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role_name: Annotated[str | None, Field(
        min_length=2, max_length=50, default=None)] = None
    status: Annotated[str | None, Field(
        pattern=r"^(Active|Inactive)$", default=None)] = None
    description: Annotated[str | None, Field(
        max_length=1000, default=None)] = None


class RoleUpdateInternal(RoleUpdate):
    updated_at: datetime


class RoleDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    deleted_at: datetime
