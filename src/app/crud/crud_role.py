from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD

from ..models.role import Role
from ..schemas.role import (
    RoleBase,
    RoleCreate,
    RoleDelete,
    RoleRead,
    RoleUpdate,
    RoleUpdateInternal
)

CRUDRole = FastCRUD[
    RoleBase,
    RoleCreate,
    RoleDelete,
    RoleRead,
    RoleUpdate,
    RoleUpdateInternal
]
crud_role = CRUDRole(Role)


async def create_with_audit(db: AsyncSession, object: RoleCreate) -> Role:
    obj_in_data = object.model_dump()
    db_obj = Role(
        **obj_in_data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
