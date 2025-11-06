from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings
from core.database.schemas.like import LikeCountResponse
from core.dependency.services import get_post_like_comment_service
from core.services.PLC import PostLikeCommentService


router = APIRouter(
    prefix=settings.api.like,
    tags=["Like"],
)


@router.post("/post/{post_id}")
async def like_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.like_post(user_id=user.id, post_id=post_id)


@router.get("/post/{post_id}")
async def get_post_likes(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    """
    Display a list of users who liked the post
    """
    return await service.get_post_likes(post_id=post_id)


@router.delete("/post/{post_id}")
async def unlike_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.unlike_post(user_id=user.id, post_id=post_id)


@router.post("/comment/{comment_id}")
async def like_comment(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.like_comment(user_id=user.id, comment_id=comment_id)


@router.delete("/comment/{comment_id}")
async def unlike_comment(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.unlike_comment(user_id=user.id, comment_id=comment_id)


@router.get("/comment/{comment_id}")
async def get_comment_likes(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    """
    Display a list of users who liked the comment
    """
    return await service.get_comment_likes(comment_id=comment_id)
