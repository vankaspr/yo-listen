from fastapi import APIRouter, Depends
from typing import Annotated

from core.config import settings
from core.database.models import User
from core.services import AdminService, PostLikeCommentService
from core.dependency.admin import get_current_superuser
from core.dependency.services import (
    get_admin_service,
    get_post_like_comment_service,
)

router = APIRouter(prefix=settings.api.admin, tags=["Admin"])

# ------------------------ Users data and statistics --------------------


@router.get("/statistic/users")
async def statistics(
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.get_user_stats()


@router.get("/statistic/users/new/{days}")
async def statistic_of_new_users(
    days: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.get_new_users(days=days)


@router.get("/statistic/users/all/unverified/{days}")
async def unverified_statistic(
    days: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.get_unverified_old_users(days=days)


@router.get("/statistic/users/all/good")
async def all_good_users(
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.get_all_active_and_verified_users()


@router.get("/info/{user_id}")
async def full_info_about_user(
    user_id: int,
    superuser: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await service.info(user_id=user_id)


# ------------------------- Action --------------------------------------


@router.patch("/deactivate/{user_id}")
async def deactivate_user(
    user_id: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.deactivate_user(user_id=user_id)


@router.patch("/reactivate/{user_id}")
async def reactivate_user(
    user_id: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.reactivate_user(user_id=user_id)


@router.delete("/delete/user/{user_id}")
async def delete_user(
    user_id: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service),
    ],
):
    return await admin_service.delete_user(user_id=user_id)


@router.delete("/delete/post/{post_id}")
async def delete_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.delete_post(user_id=user.id, post_id=post_id)


@router.delete("/delete/comment/{comment_id}")
async def delete_comment(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_superuser),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.delete_comment(user_id=user.id, comment_id=comment_id)
