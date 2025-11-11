import logging
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from core.services.base import BaseService
from core.services.user import UserService
from core.database.models import Subscription, User
from exceptions import error

logger = logging.getLogger(__name__)


class SubscriptionService(BaseService):
    """ 
    Subscription management service
    """
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session=session)
        self.user_service = UserService(session=session)

    async def _subscription_already_exists(
        self,
        follower_id: int,
        following_id: int,
    ) -> bool:
        """
        Check if subscription already exists
        """
        stmt = select(Subscription).where(
            Subscription.follower_id == follower_id,
            Subscription.following_id == following_id,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def _can_subscribe(
        self,
        follower_id: int,
        following_id: int,
    ) -> None:
        """
        Validate subscription creation
        Raises appropriate exceptions if validation fails
        """

        # cannot follow yourself
        if follower_id == following_id:
            raise error.NotAllowed("Cannot follow yourself")

        # following user not found or user is not active
        user = await self.user_service.get_user_by_id(user_id=following_id)

        if not user:
            raise error.NotFound("User not found")

        if not user.is_active:
            raise error.NotAllowed("Cannot follow inactive user")

        # check if subscribe already exist
        if await self._subscription_already_exists(
            follower_id=follower_id,
            following_id=following_id,
        ):
            raise error.NotAllowed("Already following this user")

    async def create_subscription(
        self,
        follower_id: int,
        following_id: int,
    ) -> Subscription:
        """
        Follow a user

        follower_id: who
        following_id: on whom

        Returns: Subscription instance
        """
        try:
            # validate before creating
            await self._can_subscribe(
                follower_id=follower_id,
                following_id=following_id,
            )

            # create
            subscription = Subscription(
                follower_id=follower_id,
                following_id=following_id,
            )

            self.session.add(subscription)
            await self.session.commit()
            await self.session.refresh(subscription)

            logger.info(
                """
                User %s followed user %s
                """,
                follower_id,
                following_id,
            )

            return subscription

        except (error.NotAllowed, error.NotFound):
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def delete_subsription(
        self,
        follower_id: int,
        following_id: int,
    ) -> bool:
        """
        Delete subscription
        return bollean true if successfully delete
        """
        try:
            stmt = select(Subscription).where(
                Subscription.follower_id == follower_id,
                Subscription.following_id == following_id,
            )

            result = await self.session.execute(stmt)
            subscription = result.scalar_one_or_none()

            if not subscription:
                return False

            await self.session.delete(subscription)
            await self.session.commit()

            logger.info(
                """
                User %s unfollowed user %s
                """,
                follower_id,
                following_id,
            )

            return True

        except SQLAlchemyError as e:
            self.session.rollback()
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_user_followers(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:
        """
        Get list of users who follow the specified user
        """

        try:
            stmt = (
                select(User)
                .join(Subscription, User.id == Subscription.follower_id)
                .where(
                    Subscription.following_id == user_id,
                    User.is_active == True,
                )
                .order_by(desc(Subscription.created_at))
                .offset(skip)
                .limit(limit)
                .options(selectinload(User.profile))
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_user_following(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:
        """
        Get list of users that the specified user is following

        Returns: List of User objects that the user follows
        """
        try:
            stmt = (
                select(User)
                .join(
                    Subscription,
                    User.id == Subscription.following_id,
                )
                .where(
                    Subscription.follower_id == user_id,
                    User.is_active == True,
                )
                .order_by(desc(Subscription.created_at))
                .offset(skip)
                .limit(limit)
                .options(selectinload(User.profile))
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_subscriptions_stats(
        self,
        user_id: int,
    ) -> dict:
        """
        Get subscription statistics for a user
        Returns dict {
            followers_count
            following_count

        }
        """
        try:
            followers = select(func.count(Subscription.id)).where(
                Subscription.following_id == user_id
            )

            followers_count = await self.session.scalar(followers) or 0

            following = select(func.count(Subscription.id)).where(
                Subscription.follower_id == user_id
            )

            following_count = await self.session.scalar(following) or 0

            return {
                "followers_count": followers_count,
                "following_count": following_count,
            }
        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e
