from pydantic import BaseModel

class BioUpdate(BaseModel):
    bio: str | None = None
    
class AvatarUpdate(BaseModel):
    avatar: str | None = None 