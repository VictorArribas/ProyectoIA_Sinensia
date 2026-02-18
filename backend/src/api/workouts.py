"""
Workouts API Endpoints
POST /api/v1/workouts/generate - Generate new workout plan (calls Claude AI)
GET /api/v1/workouts/history - Get workout history
GET /api/v1/workouts/{workout_plan_id} - Get specific workout plan
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.middleware.auth_middleware import get_current_user
from src.models.user import User
from src.schemas.workout import (
    WorkoutGenerateRequest,
    WorkoutPlanResponse,
    WorkoutHistoryItem,
    WorkoutPlanDetail,
)
from src.services.workout_service import WorkoutService

router = APIRouter(prefix="/api/v1/workouts", tags=["workouts"])


@router.post("/generate", response_model=WorkoutPlanResponse)
async def generate_workout(
    request: WorkoutGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate personalized workout plan using Claude AI

    - Requires user profile to exist
    - Optional fatigue_score (0-100, defaults to 50)
    - Returns structured workout plan with exercises, sets, reps, RPE
    - Includes medical disclaimer

    This endpoint calls Anthropic Claude API and may take 5-10 seconds

    Requires authentication
    """
    try:
        workout_plan = await WorkoutService.generate_workout_plan(db, current_user, request)

        # Return the plan_data as WorkoutPlanResponse
        return WorkoutPlanResponse(**workout_plan.plan_data)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate workout plan: {str(e)}",
        )


@router.get("/history", response_model=List[WorkoutHistoryItem])
async def get_workout_history(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Get user's workout plan history (last 30 plans)

    Returns list of workout summaries with:
    - id
    - created_at
    - fatigue_score_used
    - exercise_count

    Requires authentication
    """
    history = await WorkoutService.get_workout_history(db, current_user, limit=30)
    return history


@router.get("/{workout_plan_id}", response_model=WorkoutPlanDetail)
async def get_workout_plan(
    workout_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get specific workout plan by ID

    Returns full workout plan with all exercise details

    Requires authentication and plan ownership
    """
    workout_plan = await WorkoutService.get_workout_plan_by_id(db, current_user, workout_plan_id)

    if not workout_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found or you don't have access",
        )

    # Build response
    plan_data = workout_plan.plan_data
    return WorkoutPlanDetail(
        id=workout_plan.id,
        user_id=workout_plan.user_id,
        workout_plan=plan_data.get("workout_plan", []),
        disclaimer_medico=plan_data.get("disclaimer_medico", ""),
        fatiga_score_usado=workout_plan.fatigue_score_used,
        ajuste_aplicado=plan_data.get("ajuste_aplicado"),
        created_at=workout_plan.created_at,
    )
