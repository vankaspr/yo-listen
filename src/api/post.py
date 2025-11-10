from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings
from core.database.schemas.post import PostResponse, PostCreate, PostUpdate
from core.dependency.services import get_post_like_comment_service
from core.services.PLC import PostLikeCommentService

router = APIRouter(
    prefix=settings.api.post,
    tags=["Post"],
)


@router.post("/create", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[PostLikeCommentService, Depends(get_post_like_comment_service)],
):
    post = await service.create_post(
        user_id=user.id,
        title=post_data.title,
        content=post_data.content,
        tag=post_data.tag,
    )

    return post


@router.get("/")
async def get_posts(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_all_user_posts(user_id=user.id)


@router.get("/search/id/{post_id}")
async def get_post(
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
    return await service.get_post_by_id(post_id=post_id)


@router.get("/search/tag/{tag}")
async def get_posts_by_tag(
    tag: str,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_posts_by_tag(tag=tag)


@router.patch("/{post_id}")
async def update_post(
    post_id: int,
    update_data: PostUpdate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):

    update_dict = update_data.model_dump(exclude_unset=True)

    return await service.update_post(
        post_id=post_id,
        user_id=user.id,
        **update_dict,
    )


@router.delete("/{post_id}")
async def delete_post(
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
    return await service.delete_post(user_id=user.id, post_id=post_id)
