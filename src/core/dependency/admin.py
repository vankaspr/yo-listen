from typing import Annotated
from fastapi import Depends

from core.database.models import User
from exceptions.error import NotAllowed
from .user import get_current_user


async def get_current_superuser(
    user: Annotated[
        User,
        Depends(get_current_user)
    ]
) -> User:
    if not user.is_superuser:
        raise NotAllowed("Access denied. You are a civilian.")
    return user