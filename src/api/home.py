from fastapi import APIRouter, Depends
from typing import Annotated
from core.config import settings
from core.dependency.services import get_post_like_comment_service, get_user_service
from core.services.PLC import PostLikeCommentService
from core.services.user import UserService




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



@router.get("/stats")
async def site_stats(
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service)
    ],
    service_user: Annotated[
        UserService,
        Depends(get_user_service)
    ]
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