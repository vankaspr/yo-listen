from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user
from core.config import settings

router = APIRouter(
    prefix=settings.api.post,
    tags=["Post"],
)


@router.post("/create")
async def create_post(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.get("/")
async def get_posts(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.patch("/{post_id}")
async def update_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    pass
