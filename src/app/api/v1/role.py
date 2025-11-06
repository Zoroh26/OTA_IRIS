from datetime import UTC, datetime
from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_role import crud_role
from ...schemas.role import RoleRead

router = APIRouter(tags=["role"])


@router.get("/roles", response_model=PaginatedListResponse[RoleRead])
async def get_roles(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10
) -> dict:
    roles_data = await crud_role.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=RoleRead
    )
    response: dict[str, Any] = paginated_response(
        crud_data=roles_data, page=page, items_per_page=items_per_page
    )
    return response


@router.get("/role/{role_id}", response_model=RoleRead)
async def get_role(
    request: Request,
    role_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> RoleRead:
    role = await crud_role.get(
        db=db,
        role_id=role_id,
        schema_to_select=RoleRead
    )
    if role is None:
        raise NotFoundException('Role not found')
    return cast(RoleRead, role)
