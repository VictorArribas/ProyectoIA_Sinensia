"""
Pydantic Schemas for User Profile
"""
from typing import List, Optional
from pydantic import BaseModel, Field

from src.models.user_profile import FitnessObjective, ExperienceLevel


class UserProfileCreate(BaseModel):
    """Create user profile request"""

    age: int = Field(..., ge=13, le=120)
    weight_kg: float = Field(..., gt=0, le=500)
    height_cm: float = Field(..., gt=0, le=300)
    objective: FitnessObjective
    experience_level: ExperienceLevel
    training_days_per_week: int = Field(..., ge=1, le=7)
    equipment_available: List[str] = Field(..., min_items=1)
    injury_history: Optional[List[str]] = Field(default_factory=list)


class UserProfileUpdate(BaseModel):
    """Update user profile request (all fields optional)"""

    age: Optional[int] = Field(None, ge=13, le=120)
    weight_kg: Optional[float] = Field(None, gt=0, le=500)
    height_cm: Optional[float] = Field(None, gt=0, le=300)
    objective: Optional[FitnessObjective] = None
    experience_level: Optional[ExperienceLevel] = None
    training_days_per_week: Optional[int] = Field(None, ge=1, le=7)
    equipment_available: Optional[List[str]] = Field(None, min_items=1)
    injury_history: Optional[List[str]] = None


class UserProfileResponse(BaseModel):
    """User profile response"""

    id: int
    user_id: int
    age: int
    weight_kg: float
    height_cm: float
    objective: FitnessObjective
    experience_level: ExperienceLevel
    training_days_per_week: int
    equipment_available: List[str]
    injury_history: List[str]

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
