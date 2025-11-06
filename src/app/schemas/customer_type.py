from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CustomerTypeBase(BaseModel):
    type_name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            pattern=r"^[A-Za-z0-9 \-_]+$",
            examples=["Enterprise", "SMB", "Individual"],
        ),
    ]
    status: Annotated[
        str,
        Field(
            pattern=r"^(Active|Inactive)$",
            examples=["Active"],
            default="Active",
        ),
    ] = "Active"
    description: Annotated[
        str | None,
        Field(max_length=1000, examples=[
              "Large enterprise customer"], default=None),
    ] = None


class CustomerTypeCreate(CustomerTypeBase):
    model_config = ConfigDict(extra="forbid")


class CustomerTypeRead(CustomerTypeBase):
    customer_type_id: int
    created_at: datetime
    created_by: int
    updated_at: datetime
    updated_by: int

    model_config = ConfigDict(from_attributes=True)


class CustomerTypeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type_name: Annotated[
        str | None,
        Field(
            min_length=2,
            max_length=50,
            pattern=r"^[A-Za-z0-9 \-_]+$",
            examples=["Enterprise"],
            default=None,
        ),
    ] = None
    status: Annotated[
        str | None,
        Field(
            pattern=r"^(Active|Inactive)$",
            examples=["Inactive"],
            default=None,
        ),
    ] = None
    description: Annotated[
        str | None,
        Field(max_length=1000, examples=["Updated description"], default=None),
    ] = None


class CustomerTypeUpdateInternal(CustomerTypeUpdate):
    updated_at: datetime
    updated_by: int
    model_config = ConfigDict(extra="allow")


class CustomerTypeDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
