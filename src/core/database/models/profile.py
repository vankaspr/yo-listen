from core.database import Base
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship 

class Profile(Base):
    __tablename__ = "profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        )
    
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    
    theme: Mapped[str] = mapped_column(String, default="light")
    
    user: Mapped["User"] = relationship("User", back_populates="profile")
    
    
    