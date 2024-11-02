from fastapi import APIRouter

from api.v1.endpoints.user import router as payroll_router
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.task import router as task_router

router = APIRouter()

router.include_router(payroll_router, prefix="/payroll", tags=["Payroll"])
router.include_router(auth_router, tags=["Auth"])
router.include_router(task_router, prefix="/tasks", tags=["Tasks"])
