from fastapi import APIRouter
from core.config import settings
from .auth import router as auth_router
from .user import router as user_router
from .admin import router as admin_router
from .post import router as post_router
from .like import router as like_router
from .comment import router as comment_router
from .home import router as home_router

router = APIRouter(
    prefix=settings.api.prefix
)

router.include_router(home_router)

router.include_router(auth_router)
router.include_router(user_router)

router.include_router(post_router)
router.include_router(like_router)
router.include_router(comment_router)

router.include_router(admin_router)