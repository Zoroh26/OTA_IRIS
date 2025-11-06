from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD

from ..models.customer_type import CustomerType
from ..schemas.customer_type import (
    CustomerTypeCreate,
    CustomerTypeDelete,
    CustomerTypeRead,
    CustomerTypeUpdate,
    CustomerTypeUpdateInternal,
)

CRUDCustomerType = FastCRUD[
    CustomerType,
    CustomerTypeCreate,
    CustomerTypeDelete,
    CustomerTypeRead,
    CustomerTypeUpdate,
    CustomerTypeUpdateInternal,
]
crud_customer_types = CRUDCustomerType(CustomerType)

# Custom create method to handle audit fields


async def create_with_audit(db: AsyncSession, object: CustomerTypeCreate, created_by: int, updated_by: int) -> CustomerType:
    obj_in_data = object.model_dump()
    db_obj = CustomerType(
        **obj_in_data, created_by=created_by, updated_by=updated_by)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
