from datetime import datetime
from core.database import Base
from sqlalchemy import Integer, ForeignKey, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    like_count: Mapped[int] = mapped_column(Integer, default=0)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    likes: Mapped[list["CommentLike"]] = relationship(
        "CommentLike",
        back_populates="comment",
        cascade="all, delete-orphan",  
        passive_deletes=True, 
    )
