from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings

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
):
    pass


@router.get("/post/{post_id}")
async def get_post_likes(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.delete("/post/{post_id}")
async def unlike_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass
