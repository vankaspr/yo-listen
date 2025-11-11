import logging
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from core.database.models import (
    Post,
    Like,
)
from core.services.base import BaseService

from exceptions import error


logger = logging.getLogger(__name__)


class RecommendationService(BaseService):
    """ 
    
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
