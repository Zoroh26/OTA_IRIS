from datetime import UTC, datetime
from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_customer_types import crud_customer_types
from ...schemas.customer_type import CustomerTypeCreate, CustomerTypeRead, CustomerTypeUpdate, CustomerTypeUpdateInternal

router = APIRouter(tags=["customer-types"])


@router.post("/customer-type", response_model=CustomerTypeRead, status_code=201)
async def create_customer_type(
    request: Request,
    customer_type: CustomerTypeCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
) -> CustomerTypeRead:
    existing = await crud_customer_types.exists(db=db, type_name=customer_type.type_name)
    if existing:
        raise DuplicateValueException(
            "Customer Type with this name already exists")

    # Only use fields defined in CustomerTypeCreate
    customer_type_internal = CustomerTypeCreate(**customer_type.model_dump())

    # Use custom create_with_audit method
    from ...crud.crud_customer_types import create_with_audit
    created = await create_with_audit(
        db=db,
        object=customer_type_internal,
        created_by=current_user["id"],
        updated_by=current_user["id"]
    )

    result = await crud_customer_types.get(
        db=db,
        customer_type_id=created.customer_type_id,
        schema_to_select=CustomerTypeRead
    )

    if result is None:
        raise NotFoundException("Created customer type not found")

    return result  # No need to cast, type is already correct


@router.get("/customer-types", response_model=PaginatedListResponse[CustomerTypeRead])
async def get_customer_types(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
    status: str | None = None,

) -> dict:
    """
    Get paginated list of customer types.

    **Query parameters:**
    - page: Page number (default: 1)
    - items_per_page: Number of items per page (default: 10)
    - status: Filter by status (Active or Inactive)
    """
    filters = {}
    if status:
        filters["status"] = status

    customer_types_data = await crud_customer_types.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=CustomerTypeRead,
        **filters,
    )

    response: dict[str, Any] = paginated_response(
        crud_data=customer_types_data, page=page, items_per_page=items_per_page
    )
    return response


@router.get("/customer-type/{customer_type_id}", response_model=CustomerTypeRead)
async def get_customer_type(
    request: Request,
    customer_type_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> CustomerTypeRead:
    """
    Get a specific customer type by ID.
    """
    customer_type = await crud_customer_types.get(
        db=db,
        customer_type_id=customer_type_id,
        schema_to_select=CustomerTypeRead,
    )

    if customer_type is None:
        raise NotFoundException("Customer type not found")

    return cast(CustomerTypeRead, customer_type)


@router.patch("/customer-type/{customer_type_id}", response_model=CustomerTypeRead)
async def update_customer_type(
    request: Request,
    customer_type_id: int,
    values: CustomerTypeUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
) -> CustomerTypeRead:
    db_customer_type = await crud_customer_types.get(db=db, customer_type_id=customer_type_id)
    if db_customer_type is None:
        raise NotFoundException("Customer type not found")

    if values.type_name and values.type_name != db_customer_type.type_name:
        existing = await crud_customer_types.exists(db=db, type_name=values.type_name)
        if existing:
            raise DuplicateValueException(
                "Customer type with this name already exists")

    updated_by = current_user["id"]
    values_internal = CustomerTypeUpdateInternal(
        **values.model_dump(exclude_unset=True),
        updated_by=updated_by,
        updated_at=datetime.now(UTC),
    )

    await crud_customer_types.update(
        db=db,
        object=values_internal,
        customer_type_id=customer_type_id,
    )

    updated = await crud_customer_types.get(
        db=db,
        customer_type_id=customer_type_id,
        schema_to_select=CustomerTypeRead,
    )

    if updated is None:
        raise NotFoundException("Updated customer type not found")

    return updated
