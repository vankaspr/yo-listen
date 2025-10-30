from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.services.profile import ProfileService
from core.dependency.user import get_current_user
from core.dependency.services import get_profile_service
from core.config import settings

router = APIRouter(
    prefix=settings.api.user,
    tags=["User"]
)

@router.get("/me")
async def me(
    user: Annotated[
        User,
        Depends(get_current_user)
    ]
):
    return {
        "message": "👺 - Current user info:",
        "id": user.id,
        "email": user.email, 
        "username": user.username,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_superuser": user.is_superuser,
    }
    

@router.get('/me/profile')
async def profile(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    profile_service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ]
):
    
    profile = await profile_service.get_user_profile(user.id)
    
    response_data = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
    }
    
    if profile:
        response_data.update(
            {
                "avatar": profile.avatar,
                "bio": profile.bio,
                "theme": profile.theme,
            }
        )
        message = "Here's full profile of user:"
    else:
        message = "Profile not found"
    
    
    return {
        "message": message,
        **response_data
        
    }