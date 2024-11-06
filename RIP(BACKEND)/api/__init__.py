from fastapi import APIRouter
from api.task import router as task_router
from api.chat import router as chat_router
from api.auth import router as user_router

router = APIRouter()
router.include_router(task_router)
router.include_router(chat_router)
router.include_router(user_router)