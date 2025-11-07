import logging
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.user import UserService
from core.services.profile import ProfileService
from core.database.models import User
from utilities.jwt_token import create_jwt_token
from exceptions import error
from core.config import settings

logger = logging.getLogger(__name__)

class OauthService:
    """ 
    A service for authentication using 
    third-party services (specifically GitHub).
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session)
        self.profile = ProfileService(session)
        
        
    async def authenticate(
        self, 
        code: str
    ) -> dict:
        """ 
        
        """
        # get access token from githab
        access_token = await self.get_access_token(code)
        
        # get user data
        user_data = await self.get_user_info(access_token)
        
        #find or create user
        user = await self.find_or_create_user(user_data)
        
        # finf or create profile 
        await self.profile.get_or_create_profile(user=user)
        
        # generate our token jwt 
        token = create_jwt_token(
            data={
            "sub": user.id,
            "type": "access_token",
            "username": user.username,
        })
        
        return {
            "token": token,
            "token_type": "bearer",
        }
    
    async def get_access_token(self, code: str) -> str:
        """ 
        Exchange GitHub code for access token
        """
        
        url = settings.oauth.github_url
        data = {
            "client_id": settings.oauth.client_id,
            "client_secret": settings.oauth.client_secret,
            "code": code,
            "redirect_uri": settings.oauth.redirect_uri,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                json=data,
                headers=headers
            ) as response:
                if response.status != 200:
                    err = await response.text()
                    logger.error(
                        """ 
                        GitHub token exchange failed:
                        %r
                        """, err
                    )
                    raise error.Unauthorized("Failed to get access token")
                    
                result = await response.json()
                logger.info("Parsed GitHub response: %s", result)
                
                access_token = (
                    result.get("access_token") or
                    result.get("token")
                )
                
                if not access_token:
                    logger.error("No access token found in GitHub response. Available keys: %s", list(result.keys()))
                    raise error.Unauthorized("GitHub didn't return access token")
                
                return access_token
        
        
    
    async def get_user_info(self, access_token: str) -> dict:
        """ 
        Get user info from Github API
        """
    
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=settings.oauth.github_user_url,
                headers=headers,
            ) as response:
                if response.status != 200:
                    err = await response.text()
                    logger.error(
                        """ 
                        GitHub user info failed: 
                        %r
                        """, err
                    )
                    raise error.Unauthorized("Failed to get user info")
                
                user_data = await response.json()
            
            
            if not user_data.get("email"):
                async with session.get(
                    url=settings.oauth.github_email_url,
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        emails = await response.json()
                        primary_email = next(
                            (email for email in emails if email["primary"]),
                            None
                        )
                        if primary_email:
                            user_data["email"] = primary_email["email"]
                            
            return user_data
                        
                        
    async def find_or_create_user(self, user_data: dict) -> User:
        """ 
        Find existing user or create new one from GitHub data
        """
        
        github_id = user_data["id"]
        email = user_data.get("email")
        
        
        stmt = select(User).where(User.github_id == github_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            logger.info(
                """ 
                User found by GitHub ID:
                %r
                """, github_id
            )
            return user
        
        if email:
            user = await self.user_service.get_user_by_email(email=email)
            if user:
                user.github_id = github_id
                await self.session.commit()
                logger.info(
                    """ 
                    Linked existing user with GitHub ID:
                    %r
                    """, github_id
                )
                return user
            
    
        username = user_data.get("login")
        if await self.is_username_exist(username):
            username = f"{username}_{github_id}"
        
        user = User(
            email=email or f"github_{github_id}@example.com",
            username=user_data.get("login", f"github_{github_id}"),
            is_active=True,
            hashed_password="oauth_user",
            # already verified 
            is_verified=True,
            is_superuser=False,
            github_id=github_id,

        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        logger.info(
            """ 
            Created new user from GitHub:
            %r
            """, user.username
        )
        return user
    
    
    async def is_username_exist(self, username: str) -> bool:
        """ 
        Check if username already exist 
        """
        
        stmt = select(User).where(
            User.username == username
        )
        
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        return user is not None
        
        
        
        
