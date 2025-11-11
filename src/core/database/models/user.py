from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


if TYPE_CHECKING:
    from core.database.models.subscription import Subscription
    from core.database.models.profile import Profile
    from core.database.models.comment import Comment
    from core.database.models.like import Like
    from core.database.models.like_comment import CommentLike
    from core.database.models.post import Post 


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    github_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    comment_likes: Mapped[list["CommentLike"]] = relationship(
        "CommentLike",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    following: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    followers: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.following_id]",
        back_populates="following",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
