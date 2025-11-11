from fastapi import APIRouter, Depends
from typing import Annotated
from core.config import settings
from core.dependency.services import (
    get_post_like_comment_service,
    get_user_service,
    get_recommendation_service,
)
from core.dependency.user import get_current_user
from core.services.PLC import PostLikeCommentService
from core.services.user import UserService
from core.services.recomendation import RecommendationService
from core.database.models import User


router = APIRouter(
    prefix=settings.api.home,
    tags=["Home"],
)


@router.get("/tranding-posts")
async def tranding_posts(
    limit: int,
    days: int,
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_tranding_posts_by_likes_count(
        limit=limit,
        days=days,
    )


@router.get("/tranding-users")
async def tranding_users(
    limit: int,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    return await service.get_tranding_users(limit=limit)


@router.get("/tranding-tags")
async def popular_tags(
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_tranding_tag()


@router.get("/stats")
async def site_stats(
    service: Annotated[PostLikeCommentService, Depends(get_post_like_comment_service)],
    service_user: Annotated[UserService, Depends(get_user_service)],
):
    """
    Common stats about app
    """
    users = await service_user.get_all_users_count()
    posts = await service.get_all_posts_count()
    comments = await service.get_all_comments_count()

    return {
        "message": "App stats",
        "users": users,
        "posts": posts,
        "comments": comments,
    }


@router.get("/debug/all-posts")
async def all_posts(
    limit: int,
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_all_posts(limit=limit)


@router.get("/recommendation")
async def recommendation_posts(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        RecommendationService,
        Depends(get_recommendation_service),
    ],
):
    return await service.get_recommended_posts(user_id=user.id)
