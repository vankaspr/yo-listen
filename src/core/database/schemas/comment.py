from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str
    
    
class CommentCreate(CommentBase):
    pass
    

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    post_id: int
    like_count: int
    created_at: datetime
    

class CommentWithAuthor(CommentResponse):
    author_username: str
    author_avatar: Optional[str] = None