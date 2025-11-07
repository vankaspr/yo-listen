import logging
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.services.user import UserService
from core.services.profile import ProfileService
from core.services.PLC import PostLikeCommentService
from utilities.now import get_now_date

from core.database.models import User

from exceptions import error


logger = logging.getLogger(__name__)


class AdminService:
    """
    Service for the admin and all
    the auxiliary functions that
    may be needed along the way.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user_service = UserService(session)
        self.profile_service = ProfileService(session)
        self.plc_service = PostLikeCommentService(session)

    # ------------------- USER ACTION ------------------

    async def get_count_of_all_users(self) -> int:
        """
        Get the total number of users
        """

        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_all_active_and_verified_users(
        self,
    ) -> dict[int, User]:
        """
        Get all active and verified users
        Return dict where the key is the id and the value is the user
        """

        stmt = select(User).where(User.is_verified == True, User.is_active == True)
        result = await self.session.execute(stmt)

        users = result.scalars().all()
        return {user.id: user for user in users}

    async def get_unverified_old_users(
        self,
        days: int = 7,
    ) -> list[User]:
        """
        Get unverified users older than N days
        days_old: some number of days
        return list of users
        """
        try:
            date = get_now_date(days=days)
            # date = NOW - timedelta(days=days)

            stmt = (
                select(User)
                .where(
                    User.is_verified == False,
                    User.created_at < date,
                )
                .order_by(User.created_at.desc())
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_new_users(
        self,
        days: int = 7,
    ) -> list[User]:
        """
        New users for last N days
        days: some number of days
        return list of users
        """

        date = get_now_date(days=days)
        stmt = select(User).where(
            User.created_at >= date,
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def deactivate_user(
        self,
        user_id: int,
    ) -> User:
        """
        Deactivate user by ID
        """

        user = await self.user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise error.NotFound(f"user with id {user_id} not found")

        user.is_active = False
        await self.session.commit()

        logger.info(
            """ 
            User %r deactivated by admin
            """,
            user_id,
        )

        return user

    async def reactivate_user(
        self,
        user_id: int,
    ) -> User:
        """
        Reactivate user by ID
        """

        user = await self.user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise error.NotFound(f"user with id {user_id} not found")

        user.is_active = True
        await self.session.commit()

        logger.info(
            """ 
            User %r reactivated by admin
            """,
            user_id,
        )

        return user

    async def delete_user(
        self,
        user_id: int,
    ) -> bool:
        """
        Delete user
        """
        try:
            user = await self.user_service.get_user_by_id(user_id=user_id)
            if not user:
                raise error.NotFound(f"user with id {user_id} not found")

            await self.session.delete(user)
            await self.session.commit()

            logger.info(
                """ 
                User %r permanently delete by admin
                """,
                user_id,
            )
            return True
        except SQLAlchemyError as e:
            raise error.DataBaseError("Беды с датабазе и проч. и проч.") from e

    # ------------ USER STATISTIC -------------------------

    async def get_user_stats(self) -> dict:
        """
        Shows general statistics in numbers:
        - total users,
        - total active,
        - total verified
        """
        stmt = select(
            func.count(User.id).label("total"),
            func.count(User.id).filter(User.is_active == True).label("active"),
            func.count(User.id).filter(User.is_verified == True).label("verified"),
        )

        result = await self.session.execute(stmt)
        stats = result.first()

        return {
            "total_users": stats.total,
            "active_users": stats.active,
            "verified_users": stats.verified,
        }

    # ------------------------ info ---------------------------

    async def info(
        self,
        user_id: int,
    ):
        """
        Return dict with full information about user by their ID
        """
        user = await self.user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise error.NotFound("User not found")
        profile = await self.profile_service.get_user_profile(user_id=user_id)

        posts = await self.plc_service.get_all_user_posts(user_id=user_id)

        comments = await self.plc_service.get_all_user_comments(user_id=user_id)

        return {
            "info": {
                "user": user,
                "profile": profile,
                "posts": posts,
                "comments": comments,
                
            }
        }
