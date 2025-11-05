import logging
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import Post, Like, Comment
from exceptions import error

logger = logging.getLogger(__name__)


class PostLikeCommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --------------- POST --------------------
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
        stmt = select(Post).where(Post.id == post_id)
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

    async def _is_post_owner(
        self,
        post_id: int,
        user_id: int,
    ) -> bool:
        """
        Checks that the user is the owner of the post.
        """
        post = await self.get_post_by_id(post_id=post_id)
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
        if not await self._is_post_owner(post_id=post_id, user_id=user_id):
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

        if not await self._is_post_owner(post_id=post_id, user_id=user_id):
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

        if not await self._is_post_owner(post_id=post_id, user_id=user_id):
            raise error.NotAllowed(
                "You are not the owner, you cannot edit or delete what does not belong to you."
            )

        await self.session.delete(post)
        await self.session.commit()

        logger.info(
            """ 
            Post with  %r ID permanently delete by creater
            """,
            post_id,
        )
        return True

    # ----------------------LIKE --------------------
    async def like_post(
        self,
        user_id: int,
        post_id: int,
    ) -> Like:
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

    async def unlike_post(
        self,
        user_id: int,
        post_id: int,
    ) -> bool:
        """
        Delete like
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
        return False

    async def get_post_likes(
        self,
        post_id: int,
    ) -> list[Like]:
        """
        Get all likes by post
        """
        stmt = select(Like).where(Like.post_id == post_id)
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

    # ---------------- COMMENT --------------------
    async def _is_comment_owner(
        self,
        comment_id: int,
        user_id: int,
    ) -> bool:
        """
        Checks that the user is the owner of the comment.
        """
        comment = await self.get_comment_by_id(comment_id=comment_id)
        return comment is not None and comment.user_id == user_id

    async def create_comment(
        self,
        user_id: int,
        post_id: int,
        content: str,
    ) -> Comment:
        comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content,
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
        stmt = select(Comment).where(Comment.post_id == post_id)
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

        if not await self._is_comment_owner(comment_id, user_id):
            raise error.NotAllowed("You are not the owner of this comment,you cannot edit or delete what does not belong to you.")
        
        await self.session.delete(comment)

        # comment counter
        await self._update_post_comment_count(
            post_id=comment.post_id,
            increment=False,
        )

        await self.session.commit()

        logger.info(
            """ 
            Comment with %r ID permanently delete by creater
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
        if not await self._is_comment_owner(comment_id, user_id):
            raise error.NotAllowed("You are not the owner of this comment,you cannot edit or delete what does not belong to you.")

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
