import jwt
import re
import logging


from typing import Optional
from datetime import timedelta

from fastapi import (
    Request,
    BackgroundTasks,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from core.database.schemas.user import UserCreate
from core.database.models import User, RefreshToken, Profile, Post

from utilities.now import get_now_timezone_date
from utilities.security import hash_password, verify_password
from utilities.jwt_token import create_jwt_token, verify_token

from exceptions import error

from core.mailing import (
    send_answer_after_verify,
    send_verification_email,
    send_pasword_reset_email,
    send_answer_after_reset_password,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:
    """
    Service related to users:
    creation, validation, login, etc.
    """

    def __init__(
        self, session: AsyncSession, background_task: Optional[BackgroundTasks] = None
    ):
        self.session = session
        self.background_task = background_task

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Creates a new user with a unique email and username,
        hashes the password,
        and sends a token to the email for email confirmation.
        """

        # logic for unique email and username:
        if await self.get_user_by_email(user_data.email):
            raise error.LoginAlreadyExist("Email already exist!")
        if await self.get_user_by_username(user_data.username):
            raise error.LoginAlreadyExist("Username already exist!")

        # password validation:
        await self.validate_password(user_data.password)

        # password hashing:
        hashed_password = hash_password(user_data.password)

        try:
            # create user:
            user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                is_active=True,
                is_verified=False,
                is_superuser=False,
            )

            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

            # verify email:
            await self.request_to_verify(user=user)

            return user
        except Exception as e:
            await self.session.rollback()
            raise error.InternalServerError(
                "Failed registration. Try again later or contact support"
            ) from e

    async def request_to_verify(
        self,
        user: User,
    ) -> None:
        """
        In case you need to resend the email verification token

        """
        if user.is_verified:
            raise error.LoginAlreadyExist("User already verified")

        try:
            # generate token:
            verification_token = await self.generate_verification_token(user_id=user.id)

            # send verification email:
            await self.after_request_verify(user=user, token=verification_token)

            logger.info(
                """
                📧 Verification email sent to %r:
                Token: %r
                """,
                user.email,
                verification_token,
            )
        except Exception as e:
            logger.error("Failed to send verification email: ", e)
            raise error.InternalServerError(
                "Failed to send verification email. Please contact support."
            ) from e

    async def authenticate(
        self,
        login: str,
        password: str,
    ) -> User:
        """
        Authenticates only active and verified users.
        Allows you to log in using your email or username.
        """
        if "@" in login:
            user = await self.get_user_by_email(login)
        else:
            user = await self.get_user_by_username(login)

        if not user:
            raise error.NotFound("User not found!")

        if not user.is_active:
            raise error.NotAllowed("Account is deactivated!")

        if not user.is_verified:
            raise error.NotAllowed("Email not verified!")

        # verifying password
        if not verify_password(password, user.hashed_password):
            raise error.NotValidData("Invalid password!")

        return user

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Found user by EMAIL and return User
        or if not found return None.
        """
        try:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
        except Exception as e:
            raise error.NotFound("User not found") from e

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Found user by USERNAME and return User
        or if not found return None.
        """
        try:
            stmt = select(User).where(User.username == username)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
        except Exception as e:
            raise error.NotFound("User not found") from e

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Found user by ID and return User
        or if not found return None.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
        except Exception as e:
            raise error.NotFound("User not found") from e

    async def generate_verification_token(
        self,
        user_id: int,
    ) -> str:
        """Generate verification token"""

        token_data = {"sub": str(user_id), "type": "email_verification"}

        return create_jwt_token(token_data, expires_delta=timedelta(minutes=5))

    async def after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        """
        Generates a verification link and
        sends an email to the user as a background task.
        """

        verification_link = f"http://localhost:8000/verification-proccess?token={token}"

        self.background_task.add_task(
            send_verification_email, user=user, verification_link=verification_link
        )

        logger.info(
            """
            🫴 Email was send with link:
            %r
            to user: %r
            """,
            verification_link,
            user.username,
        )

    async def verify_email_token(
        self,
        token: str,
    ):
        """
        Verifies the user using a verification token.
        Changes the verification flag to True if this is the case.
        Sends an email confirming successful verification.
        """

        try:
            payload = verify_token(token=token)

            if not payload or payload.get("type") != "email_verification":
                raise error.ErrorToken("Invalid token or missing token!")

            user_id = int(payload.get("sub"))
            user = await self.get_user_by_id(user_id)

            if not user:
                raise error.NotFound("User not found!")

            user.is_verified = True

            # create profile
            profile = Profile(user_id=user.id)
            self.session.add(profile)

            await self.session.commit()

            # sending confirm email about verification:
            self.background_task.add_task(
                send_answer_after_verify,
                user=user,
            )

            return user

        except jwt.ExpiredSignatureError as e:
            raise error.ErrorToken("Token already expired!") from e

        except jwt.InvalidTokenError as e:
            raise error.ErrorToken("Invalid token!") from e

    async def validate_password(
        self,
        password: str,
    ) -> None:
        """
        Validate password.
        Password shoub be:
        - at least 8 characters long
        - not contain only digits
        - must contain at least one uppercase letter
        - must contain at least one digit
        - must contain at least one special character
        """
        pass

        # if len(password) < 8:
        #    raise error.NotValidData("Password should be at least 8 characters long")
        # if password.isdigit():
        #    raise error.NotValidData("Password should not contain only digits")
        # if not re.search(r"[A-Z]", password):
        #    raise error.NotValidData("Password must contain at least one uppercase letter")
        # if not re.search(r"[0-9]", password):
        #    raise error.NotValidData("Password must contain at least one digit")
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        #    raise error.NotValidData("Password must contain at least one special character")

    async def forgot_password(
        self,
        email: str,
        request: Optional[Request] = None,
    ):
        """
        Generates a token and sends the user an email
        with a link containing the token's query parameter.
        """
        user = await self.get_user_by_email(email=email)

        if not user:
            raise error.NotFound("User not found!")

        if not user.is_active:
            raise error.NotAllowed("Account is deactivated!")

        if not user.is_verified:
            raise error.NotAllowed("Email not verified!")

        reset_data = {
            "sub": str(user.id),
            "type": "password_reset",
        }

        # create token
        reset_token = create_jwt_token(reset_data, expires_delta=timedelta(minutes=5))

        reset_link = f"http://localhost:8000/reset-proccess?token={reset_token}"

        # sent email
        self.background_task.add_task(
            send_pasword_reset_email,
            user=user,
            reset_link=reset_link,
        )

        logger.info(
            """
            Password reset link sent to %r:
            Reset link: %r
            Token: %r,
            """,
            email,
            reset_link,
            reset_token,
        )

    async def reset_password(
        self,
        token: str,
        new_password: str,
        request: Optional[Request] = None,
    ):
        """
        Verifies the token, finds the user by their ID,
        and hashes the new password.
        Sends a confirmation email that the password
        has been changed.

        """
        try:
            payload = verify_token(token=token)
            if not payload or payload.get("type") != "password_reset":
                raise error.ErrorToken("Invaalid token or missing token")

            user_id = int(payload.get("sub"))
            user = await self.get_user_by_id(user_id=user_id)

            if not user:
                raise error.NotFound("User not found!")

            if not user.is_active:
                raise error.NotAllowed("Account is deactivated!")

            # password validation:
            await self.validate_password(new_password)

            # check password if new pwd equal current:
            if verify_password(new_password, user.hashed_password):
                raise error.NotValidData(
                    "New password cannot be the same as the current password"
                )

            # change password
            user.hashed_password = hash_password(new_password)

            # delete refresh token for user
            await self.revoke_refresh_token(user.id)

            await self.session.commit()

            # sent email
            self.background_task.add_task(
                send_answer_after_reset_password,
                user=user,
            )

            logger.info(
                """
                Password reset succesfully for user.id: 
                - %r - !! 
                """,
                user_id,
            )
        except jwt.ExpiredSignatureError as e:
            raise error.ErrorToken("Token already expired!") from e

        except jwt.InvalidTokenError as e:
            raise error.ErrorToken("Invalid token!") from e

    async def create_refresh_token(
        self,
        user_id: int,
    ):
        try:
            token_data = {"sub": str(user_id), "type": "refresh_token"}

            NOW = get_now_timezone_date()
            expires_at = NOW + timedelta(days=30)

            token = create_jwt_token(token_data, expires_delta=timedelta(days=30))

            refresh_token = RefreshToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                is_revoked=False,
            )

            self.session.add(refresh_token)
            await self.session.commit()
            return token
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def verify_refresh_token(
        self,
        token: str,
    ) -> dict | None:
        """
        Refresh token verification
        """

        payload = verify_token(token=token, expected_type="refresh_token")

        if not payload or payload.get("type") != "refresh_token":
            raise error.ErrorToken("Mising token or invalid token!")

        return payload

    async def get_valid_refresh_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        """
        Check valid refresh token in DB
        Return token or None
        """
        try:
            NOW = get_now_timezone_date()
            stmt = select(RefreshToken).where(
                RefreshToken.token == token,
                RefreshToken.expires_at > NOW,
                RefreshToken.is_revoked == False,
            )

            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    async def validate_refresh_token(
        self,
        token: str,
    ) -> RefreshToken:
        try:
            # verify refresh token
            await self.verify_refresh_token(token=token)

            # check in DB if token is revoked
            return await self.get_valid_refresh_token(token=token)

        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
        except Exception as e:
            logger.error("Error: ", e)
            raise error.ErrorToken("Invalid token") from e

    async def revoke_refresh_token(
        self,
        user_id: int,
    ):
        """
        Revoked all refresh token for user
        """
        try:
            stmt = select(RefreshToken).where(
                RefreshToken.user_id == user_id, RefreshToken.is_revoked == False
            )

            result = await self.session.execute(stmt)
            tokens = result.scalars().all()

            for token in tokens:
                token.is_revoked = True

            await self.session.commit()

            logger.info(
                """ 
                Revoked all refresh tokens for user_id: %r
                """,
                user_id,
            )
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    # ------------------- TRAND ---------------------------
    async def get_tranding_users(
        self,
        limit: int = 20,
    ) -> list[User]:
        """
        Get users with most published posts
        """
        try:
            stmt = (
                select(User)
                .join(Post, User.id == Post.user_id)
                .where(
                    User.is_active == True,
                    User.is_verified == True,
                    Post.is_published == True,
                )
                .group_by(User.id)
                .order_by(desc(func.count(Post.id)))
                .limit(limit)
                .options(selectinload(User.profile))
            )
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e

    # -------------------- STATS -------------------------
    async def get_all_users_count(
        self,
    ) -> int:
        try:
            stmt = select(func.count(User.id)).where(
                User.is_active == True,
                User.is_verified == True,
            )
            result = await self.session.execute(stmt)
            return result.scalar() or 0
        except SQLAlchemyError as e:
            logger.error("Проснись ты обосрался. БД упала: ", e)
            raise error.DataBaseError("Database temporarily unavailable") from e
