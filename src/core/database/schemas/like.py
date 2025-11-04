from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LikeBase(BaseModel):
    post_id: int
    
class CreateLike(LikeBase):
    pass

class LikeResponse(LikeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime
    
class LikeCountResponse(BaseModel):
    post_id: int
    like_count: int
    user_liked: bool 
