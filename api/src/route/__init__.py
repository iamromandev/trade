from fastapi import APIRouter

from src.route.auth import auth_router
from src.route.health import router as health_router
from src.route.user import user_router

_subrouters = [
    health_router,
    auth_router,
    user_router,
]

router = APIRouter()

for subrouter in _subrouters:
    router.include_router(subrouter)
