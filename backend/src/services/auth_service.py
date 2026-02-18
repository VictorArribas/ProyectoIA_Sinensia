"""
Authentication Service - User registration, login, token management
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User
from src.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    async def register_user(db: AsyncSession, request: RegisterRequest) -> User:
        """
        Register a new user

        Args:
            db: Database session
            request: Registration request with email and password

        Returns:
            Created User instance

        Raises:
            ValueError: If email already registered
        """
        # Check if user exists
        result = await db.execute(select(User).where(User.email == request.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("Email already registered")

        # Create new user
        hashed_password = hash_password(request.password)
        new_user = User(email=request.email, password_hash=hashed_password)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, request: LoginRequest) -> Optional[User]:
        """
        Authenticate user by email and password

        Args:
            db: Database session
            request: Login request with email and password

        Returns:
            User instance if authentication successful, None otherwise
        """
        # Get user by email
        result = await db.execute(select(User).where(User.email == request.email))
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Verify password
        if not verify_password(request.password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """
        Create access and refresh tokens for user

        Args:
            user: User instance

        Returns:
            TokenResponse with access_token, refresh_token, token_type
        """
        token_data = {"sub": str(user.id), "email": user.email}

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
