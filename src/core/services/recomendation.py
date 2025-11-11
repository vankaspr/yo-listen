import logging
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from core.database.models import (
    Post,
    Like,
    Subscription,
)
from core.services.base import BaseService

from exceptions import error


logger = logging.getLogger(__name__)


class RecommendationService(BaseService):
    """
    Service for working with recommendations
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session=session)

    async def get_recommended_posts(
        self,
        user_id: int,
        limit: int = 20,
    ) -> list[Post]:
        try:
            # Find a popular tag for a user
            user_tags_stmt = (
                select(Post.tag, func.count(Post.id).label("tag_count"))
                .join(Like, Post.id == Like.post_id)
                .where(
                    Like.user_id == user_id,
                    Post.is_published == True,
                )
                .group_by(Post.tag)
                .order_by(desc("tag_count"))
                .limit(10)
            )

            user_tags_result = await self.session.execute(user_tags_stmt)

            if user_favorite_tags := user_tags_result.scalars().all():
                # If there are any, then we find similar tags,
                # excluding those posts that were written by the user himself.
                stmt = (
                    select(Post)
                    .where(
                        Post.is_published == True,
                        Post.tag.in_(user_favorite_tags),
                        Post.user_id != user_id,
                    )
                    .order_by(desc(Post.like_count), desc(Post.created_at))
                    .limit(limit)
                    .options(selectinload(Post.author))
                )
                logger.info("Personalized recommendations based on user tags")

            else:
                # Otherwise, we offer the user popular posts
                stmt = (
                    select(Post)
                    .where(Post.is_published == True)
                    .order_by(desc(Post.created_at))
                    .limit(limit)
                    .options(selectinload(Post.author))
                )
                logger.info("Fallback to trending posts")

            result = await self.session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            logger.error("Error getting recommended posts: %s", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_user_feed(
        self,
        user_id: int,
        limit: int = 20,
        skip: int = 0,
    ) -> list[Post]:
        """
        Get personalized feed: posts from following + recommendations
        """
        try:
            # get folowing posts feed
            following_feed = await self.get_following_post(
                user_id=user_id, skip=skip, limit=limit
            )

            # If there are few subscriptions, 
            # we supplement the feed with recommendations
            if len(following_feed) < limit:
                remaining = limit - len(following_feed)
                recommendation = await self.get_recommended_posts(
                    user_id=user_id, limit=remaining
                )
                
                feed = following_feed + recommendation
                
                #remove dublicate
                return self._deduplicate_posts(feed)
            
            return following_feed

        except SQLAlchemyError as e:
            logger.error("Error getting recommended posts: %s", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_following_post(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Post]:
        """
        A feed of posts for a specific user based on who that user follows
        """
        try:
            stmt = (
                select(Post)
                .join(Subscription, Post.user_id == Subscription.following_id)
                .where(
                    Subscription.follower_id == user_id,
                    Post.is_published == True,
                )
                .order_by(desc(Post.created_at))
                .offset(skip)
                .limit(limit)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.comments),
                    selectinload(Post.likes),
                )
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            logger.error("Error getting recommended posts: %s", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    def _deduplicate_posts(
        self,
        posts: list[Post],
    ) -> list[Post]:
        """ 
        Remove duplicated posts from feed
        """
        seen = set()
        unique_post = []
        for post in posts:
            if post.id not in seen:
                seen.add(post.id)
                unique_post.append(post)
        return unique_post
