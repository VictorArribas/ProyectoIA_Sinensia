"""
Pydantic Schemas for Workout Plans
Based on spec.md Technical Deep Dive
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ExerciseBlock(BaseModel):
    """
    Single exercise block in workout plan
    Matches Technical Deep Dive schema from spec.md
    """

    musculo: str = Field(..., min_length=3, max_length=50, description="Target muscle group")
    ejercicio: str = Field(..., min_length=3, max_length=100, description="Exercise name")
    series: int = Field(..., ge=1, le=10, description="Number of sets")
    repeticiones: str = Field(
        ..., pattern=r"^\d{1,2}(-\d{1,2})?$", description="Reps (e.g., '8-12' or '10')"
    )
    rpe_objetivo: int = Field(..., ge=1, le=10, description="Target RPE (Rate of Perceived Exertion)")
    descanso_segundos: int = Field(..., ge=30, le=600, description="Rest between sets (seconds)")
    notas_seguridad: str = Field(
        ..., min_length=10, max_length=500, description="Safety notes and technique cues"
    )


class WorkoutPlanResponse(BaseModel):
    """
    Workout plan response from LLM
    Includes plan data, disclaimer, and fatigue context
    """

    workout_plan: List[ExerciseBlock] = Field(..., min_items=3, max_items=15)
    disclaimer_medico: str = Field(
        default="Consulta con un profesional de la salud antes de iniciar cualquier programa de ejercicio. Detente inmediatamente si experimentas dolor."
    )
    fatiga_score_usado: int = Field(..., ge=0, le=100, description="Fatigue score used for generation")
    ajuste_aplicado: Optional[str] = Field(None, description="Adjustment applied based on fatigue")


class WorkoutGenerateRequest(BaseModel):
    """Request to generate a new workout plan"""

    fatigue_score: Optional[int] = Field(
        default=50, ge=0, le=100, description="Optional fatigue score (defaults to 50)"
    )


class WorkoutHistoryItem(BaseModel):
    """Workout plan in history list"""

    id: int
    created_at: datetime
    fatigue_score_used: int
    exercise_count: int  # Derived from plan_data

    class Config:
        from_attributes = True


class WorkoutPlanDetail(BaseModel):
    """Full workout plan with ID and metadata"""

    id: int
    user_id: int
    workout_plan: List[ExerciseBlock]
    disclaimer_medico: str
    fatiga_score_usado: int
    ajuste_aplicado: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
