from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    tag: str
    is_published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    
class PostList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    tag: str
    user_id: int
    like_count: int
    comment_count: int
    created_at: datetime
    

class UserPostsResponse(BaseModel):
    public_posts: list[PostResponse]
    hidden_posts: list[PostResponse]
    total_public: int
    total_hidden: int
    all_posts: int