from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.services import (
    ProfileService,
    PostLikeCommentService,
    SubscriptionService,
)
from core.dependency.user import get_current_user
from core.dependency.services import (
    get_profile_service,
    get_post_like_comment_service,
    get_subscription_service,
)
from core.config import settings
from core.database.schemas.profile import BioUpdate, AvatarUpdate

router = APIRouter(prefix=settings.api.user, tags=["User"])


@router.get("/me")
async def me(user: Annotated[User, Depends(get_current_user)]):
    return {
        "message": "👺 - Current user info:",
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_superuser": user.is_superuser,
    }


@router.get("/me/profile")
async def profile(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    profile_service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ],
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
        response_data |= {
            "avatar": profile.avatar,
            "bio": profile.bio,
            "theme": profile.theme,
        }

        message = "Here's full profile of user:"
    else:
        message = "Profile not found"

    return {"message": message, **response_data}


@router.patch("/me/profile/bio")
async def update_bio(
    update: BioUpdate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    profile_service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ],
):

    return await profile_service.update_bio(user.id, update.bio)


@router.patch("/me/profile/avatar")
async def update_avatar(
    update: AvatarUpdate,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    profile_service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ],
):

    return await profile_service.update_avatar(user.id, update.avatar)


@router.get("/me/profile/liked-post")
async def user_liked_post(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        PostLikeCommentService,
        Depends(get_post_like_comment_service),
    ],
):
    return await service.get_liked_post_by_user(user_id=user.id)


@router.post("/me/subscriptions/subscribe/{following_id}")
async def subscribe(
    following_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        SubscriptionService,
        Depends(get_subscription_service),
    ],
):
    """
    Subscribe to another user

    **following_id**: ID of the user you want to follow

    Returns the created subscription object
    """
    return await service.create_subscription(
        follower_id=user.id,
        following_id=following_id,
    )


@router.get("/me/subscriptions/following")
async def me_following(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        SubscriptionService,
        Depends(get_subscription_service),
    ],
):
    return await service.get_user_following(user_id=user.id)


@router.get("/me/subscriptions/followers")
async def my_followers(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        SubscriptionService,
        Depends(get_subscription_service),
    ],
):
    """
    Get my followers
    """
    result = await service.get_user_followers(
        user_id=user.id,
    )

    if not result:
        return {
            "message": "You don't have any subscribers yet.",
            "count": 0,
            "followers": result,
        }

    return {
        "count": len(result),
        "followers": result,
    }


@router.get("/{user_id}/follow-stats")
async def follow_stats(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        SubscriptionService,
        Depends(get_subscription_service),
    ],
):
    return await service.get_subscriptions_stats(user_id=user.id)


@router.delete("/me/subscriptions/unsubscribe/{following_id}")
async def unsubscribe(
    following_id: int,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        SubscriptionService,
        Depends(get_subscription_service),
    ],
):
    return await service.delete_subsription(
        follower_id=user.id,
        following_id=following_id,
    )
