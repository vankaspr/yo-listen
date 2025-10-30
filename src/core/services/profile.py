import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import User, Profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_user_profile(
        self,
        user_id: int
    ) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create_profile(
        self,
        user: User,
    ) -> Profile:
        profile = Profile(user_id=user.id)
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
    
    async def get_or_create_profile(
        self, 
        user: User
    ) -> Profile:
        """ 
        Get an existing profile or create new one if not
        Return profile
        """
        
        return (await self.get_user_profile(user_id=user.id) 
                or await self.create_profile(user=user))
        
    
    async def update_profile(
        self,
        user_id: int,
        update_data: dict,
    ) -> Profile:
        """ 
        Update only an existing profile
        """
        
        profile = await self.get_user_profile(user_id=user_id)
        if not profile:
            raise ValueError("Profile not found")
        
        for filed, value in update_data.items():
            if hasattr(profile, filed):
                setattr(profile, filed, value)
                
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
    
    async def update_bio(
        self,
        user_id: int,
        bio: str,
    ) -> Profile:
        """ Update user bio"""
        return await self.update_profile(user_id=user_id,update_data={"bio": bio})
    
    async def update_avatar(
    self,
    user_id: int,
    avatar: str,
    ) -> Profile:
        """ Update user avatar"""
        return await self.update_profile(user_id=user_id,update_data={"avatar": avatar})


    async def update_theme(
    self,
    user_id: int,
    theme: str,
    ) -> Profile:
        """ Update user theme"""
        return await self.update_profile(user_id=user_id,update_data={"theme": theme})

    