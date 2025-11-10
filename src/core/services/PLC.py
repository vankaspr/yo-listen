import logging
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload
from core.database.models import (
    Post,
    Like,
    Comment,
    CommentLike,
    User,
)
from utilities.now import get_now_date

from exceptions import error

logger = logging.getLogger(__name__)


class PostLikeCommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --------------- POST -------------------- #
    async def create_post(
        self,
        user_id: int,
        title: str,
        content: str,
        tag: str,
    ) -> Post:
        """
        Create post
        """
        post = Post(
            user_id=user_id,
            title=title,
            content=content,
            tag=tag,
        )
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_post_by_id(
        self,
        post_id: int,
    ) -> Post | None:
        """
        Get post by ID return post or None
        """
        stmt = select(Post).options(joinedload(Post.author)).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_filter_post(
        self,
        post_id: int,
        user_id: int,
        is_published: bool = True,
    ) -> list[Post]:
        """
        is_oublished is a flag
        found published post if True else unpublished
        return list of post
        """
        if is_published:
            stmt = select(Post).where(
                Post.id == post_id,
                Post.user_id == user_id,
                Post.is_published == True,
            )

        else:
            stmt = select(Post).where(
                Post.id == post_id,
                Post.user_id == user_id,
                Post.is_published == False,
            )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_user_posts(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> dict:
        """
        Get all user possts separated into public and hidden
        Return dict {
            "public_posts": list[Post],
            "hidden_posts": list[Post],
            "total_public": int,
            "total_hidden": int,
            "all_posts": int
        }
        """

        public_stmt = (
            select(Post)
            .where(Post.user_id == user_id, Post.is_published == True)
            .offset(skip)
            .limit(limit)
            .order_by(Post.created_at.desc())
        )

        hidden_stmt = (
            select(Post)
            .where(Post.user_id == user_id, Post.is_published == False)
            .offset(skip)
            .limit(limit)
            .order_by(Post.created_at.desc())
        )

        public_result = await self.session.execute(public_stmt)
        hidden_result = await self.session.execute(hidden_stmt)

        public_posts = public_result.scalars().all()
        hidden_posts = hidden_result.scalars().all()

        return {
            "public_posts": public_posts,
            "hidden_posts": hidden_posts,
            "total_public": len(public_posts),
            "total_hidden": len(hidden_posts),
            "all_posts": len(public_posts) + len(hidden_posts),
        }

    async def get_all_posts(
        self,
        limit: int = 100,
    ) -> list[Post]:
        """ 
        Get all posts
        """
        try:
            stmt = select(Post).where(Post.is_published == True).order_by(Post.created_at).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e
        

    async def _can_manage_post(
        self,
        post_id: int,
        user_id: int,
    ) -> bool:
        """
        Checks that the user is the owner of the post.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return False

        # admin can everything 🤌
        if user.is_superuser:
            return True

        post = await self.get_post_by_id(post_id=post_id)
        if not post:
            raise error.NotFound("Post not found")

        return post is not None and post.user_id == user_id

    async def update_post(
        self,
        user_id: int,
        post_id: int,
        **kwargs,
    ) -> Post | None:
        """
        Update post
        """
        if not await self._can_manage_post(post_id=post_id, user_id=user_id):
            raise error.NotAllowed(
                "You are not the owner, you cannot edit or delete what does not belong to you."
            )

        stmt = update(Post).where(Post.id == post_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_post_by_id(post_id=post_id)

    async def deactivate_post(
        self,
        post_id: int,
        user_id: int,
    ) -> bool:
        """
        Hide post (is_published = False)
        """

        post = await self.get_post_by_id(post_id=post_id)
        if not post:
            raise error.NotFound(f"Post with {post_id} ID not found")

        if not await self._can_manage_post(post_id=post_id, user_id=user_id):
            raise error.NotAllowed(
                "You are not the owner, you cannot edit or delete what does not belong to you."
            )

        post.is_published = False
        await self.session.commit()
        return True

    async def delete_post(
        self,
        user_id: int,
        post_id: int,
    ) -> bool:
        """
        Delete post by their ID
        return boolean
        """

        post = await self.get_post_by_id(post_id=post_id)
        if not post:
            raise error.NotFound(f"Post with {post_id} ID not found")

        if not await self._can_manage_post(post_id=post_id, user_id=user_id):
            raise error.NotAllowed(
                "You are not the owner, you cannot edit or delete what does not belong to you."
            )

        await self.session.delete(post)
        await self.session.commit()

        logger.info(
            """ 
            Post with  %r ID permanently delete by creater or admin
            """,
            post_id,
        )
        return True

    async def get_liked_post_by_user(
        self,
        user_id: int,
    ) -> list[Post]:
        """
        Get all posts that a user has liked
        """
        try:
            stmt = (
                select(Post)
                .join(Like, Post.id == Like.post_id)
                .where(
                    Like.user_id == user_id,
                    Post.is_published == True,
                )
                .order_by(desc(Like.id))
                .options(
                    selectinload(Post.author),
                )
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_posts_by_tag(
        self,
        tag: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Post]:
        """
        Found all posts by tag
        return list of posts
        """
        try:
            stmt = (
                select(Post)
                .where(Post.is_published == True, Post.tag == tag)
                .order_by(desc(Post.created_at))
                .offset(skip)
                .limit(limit)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.comments),
                )
            )
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_tranding_tag(
        self,
        limit: int = 20,
    ) -> list[dict]:
        """
        Get most popular tags by post count
        Returns: list of dicts with tag and post_count
        """
        try:
            stmt = (
                select(Post.tag, func.count(Post.id).label("post_count"))
                .where(Post.is_published == True)
                .group_by(Post.tag)
                .order_by(desc("post_count"))
                .limit(limit)
            )

            result = await self.session.execute(stmt)
            tags_data = result.all()

            return [
                {"tag": tag, "post_count": post_count} for tag, post_count in tags_data
            ]

        except SQLAlchemyError as e:
            logger.error("Error getting trending tags: %s", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    # ----------------------LIKE -------------------- #
    async def like_post(
        self,
        user_id: int,
        post_id: int,
    ) -> Like:
        """
        Create like on post
        """
        try:
            like = Like(
                user_id=user_id,
                post_id=post_id,
            )

            self.session.add(like)

            # update like count
            await self._update_post_like_count(
                post_id=post_id,
                increment=True,
            )

            await self.session.commit()
            await self.session.refresh(like)

            return like
        except IntegrityError as e:
            await self.session.rollback()
            if "unique_user_post_like" in str(e):
                raise error.NotAllowed("You have already liked this post") from e
            raise error.NotValidData("Invalid data") from e

    async def unlike_post(
        self,
        user_id: int,
        post_id: int,
    ) -> bool:
        """
        Delete like on post
        """
        stmt = delete(Like).where(
            Like.user_id == user_id,
            Like.post_id == post_id,
        )

        result = await self.session.execute(stmt)

        # like counter
        if result.rowcount > 0:

            await self._update_post_like_count(
                post_id=post_id,
                increment=False,
            )
            await self.session.commit()

            return True
        else:
            raise error.NotAllowed("You haven't liked this post yet")

    async def get_post_likes(
        self,
        post_id: int,
    ) -> list[Like]:
        """
        Get all likes by post
        """
        stmt = (
            select(Like).options(joinedload(Like.user)).where(Like.post_id == post_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def _update_post_like_count(
        self,
        post_id: int,
        increment: bool = True,
    ) -> None:
        """
        Internal method for updating the like counter
        """

        post = await self.get_post_by_id(post_id=post_id)
        if post:
            if increment:
                post.like_count += 1
            else:
                post.like_count = max(0, post.like_count - 1)

    # --------------- LIKE COMMENT --------------------------------- #

    async def _update_comment_like_count(
        self,
        comment_id: int,
        increment: bool = True,
    ) -> None:
        comment = await self.get_comment_by_id(comment_id=comment_id)
        if comment:
            if increment:
                comment.like_count += 1
            else:
                comment.like_count = max(0, comment.like_count - 1)
        else:
            raise error.NotFound("Comment not found")

    async def like_comment(
        self,
        user_id: int,
        comment_id: int,
    ) -> CommentLike:
        """
        Create like on comment
        """
        try:
            comment_like = CommentLike(
                user_id=user_id,
                comment_id=comment_id,
            )
            self.session.add(comment_like)

            # update like count
            await self._update_comment_like_count(
                comment_id=comment_id,
                increment=True,
            )

            await self.session.commit()
            await self.session.refresh(comment_like)

            return comment_like

        except IntegrityError as e:
            await self.session.rollback()
            if "unique_user_post_like" in str(e):
                raise error.NotAllowed("You have already liked this post") from e
            raise error.NotValidData("Invalid data. You cannot liked twice!") from e

    async def unlike_comment(
        self,
        user_id: int,
        comment_id: int,
    ) -> bool:
        """
        Delete like on comment
        """
        stmt = delete(CommentLike).where(
            CommentLike.user_id == user_id,
            CommentLike.comment_id == comment_id,
        )

        result = await self.session.execute(stmt)

        if result.rowcount > 0:

            await self._update_comment_like_count(
                comment_id=comment_id, increment=False
            )
            await self.session.commit()
            return True
        else:
            raise error.NotAllowed(
                "You haven't liked this comment yet or comment not found"
            )

    async def get_comment_likes(
        self,
        comment_id,
    ) -> list[CommentLike]:
        """
        Get list with all likes by comment
        """
        stmt = (
            select(CommentLike)
            .options(joinedload(CommentLike.user))
            .where(CommentLike.comment_id == comment_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # ---------------- COMMENT -------------------- #
    async def _can_manage_comment(
        self,
        comment_id: int,
        user_id: int,
    ) -> bool:
        """
        Checks that the user is the owner of the comment.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return False

        # admin can everything 🤌
        if user.is_superuser:
            return True

        comment = await self.get_comment_by_id(comment_id=comment_id)
        if not comment:
            raise error.NotFound("Comment not found")

        return comment is not None and comment.user_id == user_id

    def _validate_comment_content(self, content: str) -> None:
        """
        Validate comment content
        """
        if not content or not content.strip():
            raise error.NotValidData("Comment cannot be empty")

        stripped_content = content.strip()

        if len(stripped_content) > 1000:
            raise error.NotAllowed("Comment is too long")

    async def create_comment(
        self,
        user_id: int,
        post_id: int,
        content: str,
    ) -> Comment:

        self._validate_comment_content(content)

        comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content.strip(),
        )
        self.session.add(comment)

        # comment counter
        await self._update_post_comment_count(
            post_id=post_id,
            increment=True,
        )

        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def get_comment_by_id(
        self,
        comment_id: int,
    ) -> Comment | None:
        """
        Found a comment by ID and return comment or None
        """
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_post_comments(
        self,
        post_id: int,
    ) -> list[Comment]:
        """
        Get all comment by post
        """
        stmt = (
            select(Comment)
            .options(joinedload(Comment.author))
            .where(Comment.post_id == post_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_comment(
        self,
        comment_id: int,
        user_id: int,
    ) -> bool:
        """
        Delete comment by ID
        """

        comment = await self.get_comment_by_id(comment_id=comment_id)
        if not comment:
            raise error.NotFound(f"Comment with {comment_id} ID not found")

        if not await self._can_manage_comment(comment_id, user_id):
            raise error.NotAllowed(
                "You are not the owner of this comment,\
                you cannot edit or delete what does not belong to you."
            )

        await self.session.delete(comment)

        # comment counter
        await self._update_post_comment_count(
            post_id=comment.post_id,
            increment=False,
        )

        await self.session.commit()

        logger.info(
            """ 
            Comment with %r ID permanently delete by creater or admin
            """,
            comment_id,
        )

        return True

    async def update_comment(
        self,
        comment_id: int,
        content: str,
        user_id: int,
    ) -> Comment | None:
        """
        Update comment
        """
        if not await self._can_manage_comment(comment_id, user_id):
            raise error.NotAllowed(
                "You are not the owner of this comment,you cannot edit or delete what does not belong to you."
            )

        self._validate_comment_content(content)

        stmt = update(Comment).where(Comment.id == comment_id).values(content)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_comment_by_id(comment_id=comment_id)

    async def _update_post_comment_count(
        self, post_id: int, increment: bool = True
    ) -> None:
        """
        Internal method for updating the comment counter
        """
        post = await self.get_post_by_id(post_id=post_id)
        if post:
            if increment:
                post.comment_count += 1
            else:
                post.comment_count = max(0, post.comment_count - 1)

    async def get_all_user_comments(
        self,
        user_id: int,
    ) -> list[Comment]:
        """
        Get all user comments
        """
        stmt = (
            select(Comment)
            .where(Comment.user_id == user_id)
            .order_by(Comment.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # --------------------- TRAND --------------------------

    async def get_tranding_posts_by_likes_count(
        self,
        limit: int = 20,
        days: int = 30,
    ) -> list[Post]:
        """
        Issues several posts according to the limit
        (by default, the first 20 posts)
        for 30 days that have a large number of likes and comments
        """
        try:

            now = get_now_date(days=days)
            stmt = (
                select(Post)
                .where(
                    Post.is_published == True,
                    Post.created_at >= now,
                )
                .order_by(
                    desc(Post.like_count),
                    desc(Post.comment_count),
                    desc(Post.created_at),
                )
                .limit(limit)
                .options(selectinload(Post.author).selectinload(User.profile))
            )

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    # --------------------- STATS ------------------------------------
    async def get_all_posts_count(
        self,
    ) -> int:
        try:
            stmt = select(func.count(Post.id)).where(Post.is_published == True)
            result = await self.session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def get_all_comments_count(
        self,
    ) -> int:
        try:
            stmt = select(func.count(Comment.id))
            result = await self.session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
