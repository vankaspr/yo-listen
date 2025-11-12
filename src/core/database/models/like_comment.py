from core.database import Base
from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from core.database.models.user import User
    from core.database.models.comment import Comment
class CommentLike(Base):
    __tablename__ = "comment_likes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    
    comment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=False,
        
    )
    
    user: Mapped["User"] = relationship("User", back_populates="comment_likes")
    comment: Mapped["Comment"] = relationship("Comment", back_populates="likes")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
    )