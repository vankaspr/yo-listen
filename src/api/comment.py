from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings

router = APIRouter(
    prefix=settings.api.comment,
    tags=["Comment"],
)


@router.post("/post/{post_id}")
async def create_comment(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.patch("/{comment_id}")
async def update_comment(
    comment_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.get("/post/{post_id}")
async def get_post_comments(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass
