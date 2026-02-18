"""
Profile Service - User profile management
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User
from src.models.user_profile import UserProfile
from src.schemas.profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse


class ProfileService:
    """Service for user profile operations"""

    @staticmethod
    async def get_user_profile(db: AsyncSession, user: User) -> Optional[UserProfile]:
        """
        Get user's profile

        Args:
            db: Database session
            user: Current user

        Returns:
            UserProfile or None if not found
        """
        result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user_profile(
        db: AsyncSession, user: User, request: UserProfileCreate
    ) -> UserProfile:
        """
        Create user profile (onboarding)

        Args:
            db: Database session
            user: Current user
            request: Profile creation request

        Returns:
            Created UserProfile

        Raises:
            ValueError: If profile already exists
        """
        # Check if profile exists
        existing_profile = await ProfileService.get_user_profile(db, user)
        if existing_profile:
            raise ValueError("User profile already exists. Use PUT /update to modify.")

        # Create profile
        profile = UserProfile(user_id=user.id, **request.model_dump())

        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        return profile

    @staticmethod
    async def update_user_profile(
        db: AsyncSession, user: User, request: UserProfileUpdate
    ) -> UserProfile:
        """
        Update user profile

        Args:
            db: Database session
            user: Current user
            request: Profile update request (partial update)

        Returns:
            Updated UserProfile

        Raises:
            ValueError: If profile not found
        """
        # Get existing profile
        profile = await ProfileService.get_user_profile(db, user)
        if not profile:
            raise ValueError("User profile not found. Use POST /create first.")

        # Update fields (only non-None values)
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        await db.commit()
        await db.refresh(profile)

        return profile
