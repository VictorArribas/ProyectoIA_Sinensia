"""
Workout Service - Orchestrates workout plan generation
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.models.user import User
from src.models.user_profile import UserProfile
from src.models.workout_plan import WorkoutPlan
from src.models.exercise import Exercise
from src.schemas.workout import WorkoutPlanResponse, WorkoutGenerateRequest, WorkoutHistoryItem
from src.services.llm_service import llm_service


class WorkoutService:
    """Service for workout plan generation and management"""

    @staticmethod
    async def generate_workout_plan(
        db: AsyncSession, user: User, request: WorkoutGenerateRequest
    ) -> WorkoutPlan:
        """
        Generate personalized workout plan

        Args:
            db: Database session
            user: Current user
            request: Generation request with optional fatigue score

        Returns:
            Created WorkoutPlan instance

        Raises:
            ValueError: If user has no profile or generation fails
        """
        # Get user profile
        result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError("User profile not found. Please create profile first.")

        # Get available exercises
        result = await db.execute(select(Exercise))
        exercises = result.scalars().all()

        if not exercises:
            raise ValueError("No exercises available in database. Please seed exercises.")

        # Filter exercises by available equipment
        available_exercises = [
            ex
            for ex in exercises
            if any(equip in profile.equipment_available for equip in ["dumbbells", "barbell", "bodyweight", "cables", "machines"])
        ]

        if not available_exercises:
            available_exercises = list(exercises)  # Fallback to all

        # Call LLM to generate plan
        fatigue_score = request.fatigue_score if request.fatigue_score is not None else 50
        workout_plan_response: WorkoutPlanResponse = await llm_service.call_anthropic_claude(
            profile=profile, fatigue_score=fatigue_score, available_exercises=available_exercises
        )

        # Convert Pydantic response to JSON for storage
        plan_data = workout_plan_response.model_dump()

        # Create WorkoutPlan record
        workout_plan = WorkoutPlan(
            user_id=user.id, plan_data=plan_data, fatigue_score_used=fatigue_score
        )

        db.add(workout_plan)
        await db.commit()
        await db.refresh(workout_plan)

        return workout_plan

    @staticmethod
    async def get_workout_history(
        db: AsyncSession, user: User, limit: int = 30
    ) -> List[WorkoutHistoryItem]:
        """
        Get user's workout plan history

        Args:
            db: Database session
            user: Current user
            limit: Maximum number of plans to return

        Returns:
            List of workout history items
        """
        result = await db.execute(
            select(WorkoutPlan)
            .where(WorkoutPlan.user_id == user.id)
            .order_by(desc(WorkoutPlan.created_at))
            .limit(limit)
        )
        workout_plans = result.scalars().all()

        history = []
        for plan in workout_plans:
            history.append(
                WorkoutHistoryItem(
                    id=plan.id,
                    created_at=plan.created_at,
                    fatigue_score_used=plan.fatigue_score_used,
                    exercise_count=len(plan.plan_data.get("workout_plan", [])),
                )
            )

        return history

    @staticmethod
    async def get_workout_plan_by_id(
        db: AsyncSession, user: User, workout_plan_id: int
    ) -> Optional[WorkoutPlan]:
        """
        Get specific workout plan by ID

        Args:
            db: Database session
            user: Current user
            workout_plan_id: Workout plan ID

        Returns:
            WorkoutPlan or None if not found or not owned by user
        """
        result = await db.execute(
            select(WorkoutPlan).where(
                WorkoutPlan.id == workout_plan_id, WorkoutPlan.user_id == user.id
            )
        )
        return result.scalar_one_or_none()
