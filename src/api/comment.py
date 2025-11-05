from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings
from core.database.schemas.comment import CommentCreate, CommentUpdate
from core.dependency.services import get_post_like_comment_service
from core.services.PLC import PostLikeCommentService


router = APIRouter(
    prefix=settings.api.comment,
    tags=["Comment"],
)


@router.post("/post/{post_id}")
async def create_comment(
    post_id: int,
    data: CommentCreate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.create_comment(
        user_id=user.id, post_id=post_id, content=data.content
    )


@router.delete("/{comment_id}")
async def delete_comment(
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
    return await service.delete_comment(comment_id=comment_id, user_id=user.id)


@router.patch("/{comment_id}")
async def update_comment(
    comment_id: int,
    update_data: CommentUpdate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.update_comment(
        comment_id=comment_id,
        content=update_data.content,
        user_id=user.id,
    )


@router.get("/post/{post_id}")
async def get_post_comments(
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
    return await service.get_post_comments(post_id=post_id)
