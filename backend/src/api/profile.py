"""
Profile API Endpoints
GET /api/v1/profile/me - Get current user's profile
POST /api/v1/profile/create - Create user profile (onboarding)
PUT /api/v1/profile/update - Update user profile
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.middleware.auth_middleware import get_current_user
from src.models.user import User
from src.schemas.profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from src.services.profile_service import ProfileService

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile

    Requires authentication
    """
    profile = await ProfileService.get_user_profile(db, current_user)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create profile first.",
        )

    return profile


@router.post("/create", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    request: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create user profile (onboarding)

    Required fields:
    - age (13-120)
    - weight_kg (>0)
    - height_cm (>0)
    - objective (hypertrophy, cutting, strength, recomposition)
    - experience_level (beginner, intermediate, advanced)
    - training_days_per_week (1-7)
    - equipment_available (array, min 1 item)
    - injury_history (optional array)

    Requires authentication
    """
    try:
        profile = await ProfileService.create_user_profile(db, current_user, request)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/update", response_model=UserProfileResponse)
async def update_profile(
    request: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update user profile (partial update)

    All fields optional - only provided fields will be updated

    Requires authentication
    """
    try:
        profile = await ProfileService.update_user_profile(db, current_user, request)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
