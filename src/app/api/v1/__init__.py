from fastapi import APIRouter

from .health import router as health_router
from .login import router as login_router
from .logout import router as logout_router
from .users import router as users_router

from .customer_type import router as customer_type_router
from .role import router as role_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
router.include_router(customer_type_router)
router.include_router(role_router)
