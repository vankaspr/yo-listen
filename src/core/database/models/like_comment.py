from core.database import Base
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
        ForeignKey("comments.id"),
        nullable=False,
        
    )
    
    user: Mapped["User"] = relationship("User", back_populates="comment_likes")
    comment: Mapped["Comment"] = relationship("Comment", back_populates="likes")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
    )