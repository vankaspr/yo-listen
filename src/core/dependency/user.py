from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from core.database import db_helper
from utilities.jwt_token import verify_token
from core.services.user import UserService
from .transport import security
from exceptions import error


async def get_current_user(
    token: Annotated[
        str,
        Depends(security),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> User:

    payload = verify_token(token.credentials, expected_type="access_token")
    if not payload:
        raise error.Unauthorized("Invalid token or missing token")

    user_id_str: str = payload.get("sub")
    if not user_id_str:
        raise error.Unauthorized("Missing user ID in token")

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError) as e:
        raise error.Unauthorized("Invalid user ID format") from e

    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise error.NotFound("User not found")

    if not user.is_active:
        raise error.NotAllowed("Account deactivated")

    return user
