"""
LLM Service - Anthropic Claude API Integration
Generates workout plans based on user profile and fatigue score
"""
import json
from typing import Dict, List
from anthropic import Anthropic

from src.core.config import settings
from src.models.user_profile import UserProfile, FitnessObjective, ExperienceLevel
from src.models.exercise import Exercise
from src.schemas.workout import ExerciseBlock, WorkoutPlanResponse


class LLMService:
    """Service for Claude AI interactions"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def build_llm_prompt(
        self,
        profile: UserProfile,
        fatigue_score: int,
        available_exercises: List[Exercise],
    ) -> str:
        """
        Build prompt for Claude with user profile and fatigue context

        Args:
            profile: User's fitness profile
            fatigue_score: Current fatigue score (0-100)
            available_exercises: List of exercises from database

        Returns:
            Formatted prompt string
        """
        # Map objective to Spanish
        objective_map = {
            FitnessObjective.HYPERTROPHY: "Hipertrofia (ganancia muscular)",
            FitnessObjective.CUTTING: "Definición (pérdida de grasa)",
            FitnessObjective.STRENGTH: "Fuerza máxima",
            FitnessObjective.RECOMPOSITION: "Recomposición corporal",
        }

        experience_map = {
            ExperienceLevel.BEGINNER: "Principiante",
            ExperienceLevel.INTERMEDIATE: "Intermedio",
            ExperienceLevel.ADVANCED: "Avanzado",
        }

        # Build exercise library section
        exercises_text = "\n".join(
            [
                f"- {ex.name} ({', '.join(ex.muscle_groups)}): {ex.safety_notes}"
                for ex in available_exercises[:50]  # Limit to 50 for context
            ]
        )

        # Fatigue adjustment guidance
        fatigue_guidance = ""
        if fatigue_score > 80:
            fatigue_guidance = "⚠️ FATIGA ALTA (>80): Reduce volumen 30%. RPE -2 puntos. Considera semana de descarga."
        elif fatigue_score > 60:
            fatigue_guidance = "⚠️ FATIGA MODERADA-ALTA (60-80): Reduce volumen 15%. Mantén RPE pero reduce series."
        elif fatigue_score < 40:
            fatigue_guidance = "✅ FATIGA BAJA (<40): Usuario está fresco. Puedes aumentar intensidad +5-10%."
        else:
            fatigue_guidance = "✅ FATIGA NORMAL (40-60): Mantén volumen e intensidad estándar."

        prompt = f"""Eres un entrenador personal experto. Genera un plan de entrenamiento personalizado para hoy.

**PERFIL DEL USUARIO:**
- Edad: {profile.age} años
- Peso: {profile.weight_kg} kg, Altura: {profile.height_cm} cm
- Objetivo: {objective_map[profile.objective]}
- Experiencia: {experience_map[profile.experience_level]}
- Días de entrenamiento/semana: {profile.training_days_per_week}
- Equipamiento disponible: {', '.join(profile.equipment_available)}
- Lesiones/historial: {', '.join(profile.injury_history) if profile.injury_history else 'Ninguna'}

**CONTEXTO DE FATIGA:**
- Score de fatiga: {fatigue_score}/100
- {fatigue_guidance}

**BIBLIOTECA DE EJERCICIOS DISPONIBLES:**
{exercises_text}

**INSTRUCCIONES:**
1. Diseña un entreno COMPLETO para hoy (todo el cuerpo o split según experiencia)
2. Selecciona 6-12 ejercicios de la biblioteca
3. Ajusta volumen e intensidad según el score de fatiga
4. Para principiantes: enfoque en ejercicios básicos, técnica, RPE 6-7
5. Para avanzados: ejercicios complejos, mayor volumen, RPE 7-9
6. Respeta las contraindicaciones de lesiones
7. Usa solo equipamiento disponible

**FORMATO DE RESPUESTA (JSON estricto):**
{{
  "workout_plan": [
    {{
      "musculo": "nombre del músculo",
      "ejercicio": "nombre exacto del ejercicio",
      "series": 3,
      "repeticiones": "8-12",
      "rpe_objetivo": 7,
      "descanso_segundos": 90,
      "notas_seguridad": "Técnica y precauciones"
    }}
  ],
  "disclaimer_medico": "Consulta con un profesional de la salud antes de iniciar cualquier programa de ejercicio. Detente inmediatamente si experimentas dolor.",
  "fatiga_score_usado": {fatigue_score},
  "ajuste_aplicado": "Descripción breve del ajuste hecho por fatiga (o null si no aplica)"
}}

Genera el plan ahora en formato JSON válido:"""

        return prompt

    async def call_anthropic_claude(
        self, profile: UserProfile, fatigue_score: int, available_exercises: List[Exercise]
    ) -> WorkoutPlanResponse:
        """
        Call Claude API to generate workout plan

        Args:
            profile: User profile
            fatigue_score: Fatigue score (0-100)
            available_exercises: Available exercises from DB

        Returns:
            WorkoutPlanResponse with validated plan

        Raises:
            ValueError: If response parsing fails
        """
        prompt = self.build_llm_prompt(profile, fatigue_score, available_exercises)

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract response text
            response_text = message.content[0].text

            # Parse JSON response
            # Try to find JSON in code blocks first
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            # Parse JSON
            response_data = json.loads(response_text)

            # Validate with Pydantic
            workout_plan = WorkoutPlanResponse(**response_data)

            return workout_plan

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Claude response as JSON: {e}")
        except Exception as e:
            raise ValueError(f"Error calling Claude API: {e}")


# Global LLM service instance
llm_service = LLMService()
