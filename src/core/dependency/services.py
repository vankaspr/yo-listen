from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.database import db_helper
from core.services import (
    UserService,
    AdminService,
    ProfileService,
    OauthService,
    PostLikeCommentService,
)
async def get_user_service(
    background_task: BackgroundTasks,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
        ]
) -> UserService:
    return UserService(
        session=session,
        background_task=background_task
        )
    
    
async def get_admin_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
) -> AdminService:
    return AdminService(session=session)


async def get_oauth_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],   
) -> OauthService:
    return OauthService(session=session)


async def get_profile_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> ProfileService:
    return ProfileService(session=session)


async def get_post_like_comment_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> PostLikeCommentService:
    return PostLikeCommentService(session=session)
