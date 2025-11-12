import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from core.services.base import BaseService
from core.database.models import Notification, User
from exceptions import error
from core.database import db_helper

logger = logging.getLogger(__name__)


class NotificationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    # TODO: update NotificationService
    async def create_notification(
        self,
        user_id: int,
        action_by_id: int,
        type: str,
        related_to_id: int = None,
    ) -> Notification:
        """
        Create notification
        """
        try:
            logger.info(
                f"Creating notification: user_id={user_id}, action_by_id={action_by_id}, type={type}"
            )

            notification = Notification(
                user_id=user_id,
                action_by_id=action_by_id,
                related_to_id=related_to_id,
                type=type,
            )

            self.session.add(notification)
            await self.session.commit()
            await self.session.refresh(notification)

            logger.info(f"Notification created successfully: id={notification.id}")
            return notification

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("Error notification")
            raise error.DataBaseError("Database temporarily unavailable ") from e

    async def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> list[Notification]:
        """
        Receive all user notifications
        If the unread_only is True,
        we receive only unread notifications.
        """
        try:
            stmt = select(Notification).where(Notification.user_id == user_id)

            if unread_only:
                stmt = stmt.where(Notification.is_read == False)

            stmt = (
                stmt.order_by(desc(Notification.created_at))
                .offset(skip)
                .limit(limit)
                .options(
                    selectinload(Notification.actor),
                    selectinload(Notification.actor).selectinload(User.profile),
                )
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            logger.error("Error notification")
            raise error.DataBaseError("Database temporarily unavailable ") from e


async def _create_notification(
    user_id: int,
    action_by_id: int,
    type: str,
    related_to_id: int = None,
):
    async with db_helper.session_factory() as session:
        try:
            notification = NotificationService(session=session)
            await notification.create_notification(
                user_id=user_id,
                action_by_id=action_by_id,
                type=type,
                related_to_id=related_to_id,
            )
            
            await session.commit()
        except Exception as e:
            logger.error("Background notification failed:", e)
