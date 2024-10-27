from fastapi import APIRouter

from api.v1.endpoints.users import router as payroll_router
from api.v1.endpoints.auth import router as auth_router

router = APIRouter()

router.include_router(payroll_router, prefix="/payroll", tags=["Payroll"])
router.include_router(auth_router, tags=["Auth"])
