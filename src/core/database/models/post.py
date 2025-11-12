from datetime import datetime
from typing import TYPE_CHECKING
from core.database import Base
from sqlalchemy import String, Boolean, DateTime, func, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from core.database.models.user import User
    from core.database.models.like import Like
    from core.database.models.comment import Comment

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id")
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tag: Mapped[str] = mapped_column(String(100), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    comment_count: Mapped[int] = mapped_column(Integer, default=0)
    
    author: Mapped["User"] = relationship("User", back_populates="posts")
    likes: Mapped["Like"] = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments: Mapped["Comment"] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    
