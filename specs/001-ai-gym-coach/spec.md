# Feature Specification: Smart AI Gym Coach (SAIGC)

**Feature Branch**: `001-ai-gym-coach`
**Created**: 2026-02-17
**Status**: Draft
**Input**: User description: "Smart AI Gym Coach - Entrenador personal basado en LLM que gestiona el entrenamiento y la recuperación de forma dinámica"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Profile & Workout Plan Generation (Priority: P1)

A user completes their fitness profile (objective, experience level, available equipment) and receives a personalized workout routine that respects evidence-based volume recommendations for their goals.

**Why this priority**: This is the core value proposition - users cannot benefit from an AI coach without getting a workout plan. This is the minimum viable product that delivers immediate value.

**Independent Test**: Can be fully tested by creating a profile, selecting an objective (e.g., hypertrophy), and receiving a structured workout plan in table format. Success = user receives a valid, personalized routine.

**Acceptance Scenarios**:

1. **Given** a new user opens the application, **When** they complete the onboarding questionnaire (age, weight, fitness level, objective, available days per week), **Then** the system generates their initial fitness profile
2. **Given** a user has completed their profile, **When** they request a workout plan, **Then** the system displays a weekly routine in table format showing exercises, sets, reps, and rest periods appropriate for their level
3. **Given** a beginner selects "hypertrophy" as their objective, **When** the plan is generated, **Then** the routine includes 10-20 sets per muscle group per week (evidence-based volume for beginners)
4. **Given** an advanced user selects "strength" as their objective, **When** the plan is generated, **Then** the routine prioritizes compound movements (squat, bench, deadlift) with lower rep ranges (1-6 reps)
5. **Given** any user receives a workout plan, **When** they view it, **Then** they see a medical disclaimer stating "Consult with a healthcare professional before starting any exercise program. Stop immediately if you experience pain."

---

### User Story 2 - Fatigue Management & Adaptive Training (Priority: P2)

After completing a workout, a user logs their perceived exertion (RPE) and any pain/discomfort. The system automatically adjusts the intensity of their next session to prevent overtraining and injury.

**Why this priority**: This is what makes the coach "smart" and safe. It directly implements Constitution Principle VII (Safety First) and distinguishes this from static workout plans.

**Independent Test**: Can be tested by logging a workout with high fatigue/pain indicators and verifying that the next session reduces volume or intensity. Delivers value by preventing overtraining.

**Acceptance Scenarios**:

1. **Given** a user completes a workout, **When** they access the post-workout log, **Then** they are prompted to rate RPE (1-10 scale) and report any pain or discomfort (yes/no + location)
2. **Given** a user logs RPE of 9-10 or reports joint pain, **When** the next workout is generated, **Then** the system reduces volume by 20-30% and displays a warning: "Your recent session indicated high fatigue. We've reduced intensity. If pain persists, consult a healthcare professional."
3. **Given** a user consistently logs RPE of 3-5 for 2+ weeks, **When** the next workout is generated, **Then** the system increases volume or intensity by 5-10% (progressive overload)
4. **Given** a user reports chronic fatigue (high RPE for 3+ consecutive sessions), **When** they request a new workout, **Then** the system suggests a deload week (50% volume reduction) and recommends medical consultation
5. **Given** a user reports joint pain in a specific area (e.g., shoulder), **When** the next workout is generated, **Then** exercises stressing that joint are removed or substituted with safer alternatives

---

### User Story 3 - Nutrition Calculator (Priority: P3)

A user inputs their weight, activity level, and fitness objective to receive personalized macro recommendations (protein, carbs, fats) that update automatically when their weight changes.

**Why this priority**: Nutrition is critical for results but the workout plan can function independently. Users can still train effectively while learning nutrition separately.

**Independent Test**: Can be tested by entering profile data, receiving macro targets, then updating weight and verifying that recommendations recalculate. Delivers standalone value for diet planning.

**Acceptance Scenarios**:

1. **Given** a user has completed their fitness profile, **When** they access the nutrition module, **Then** they see calculated macro targets (grams of protein, carbs, fats) based on their TDEE (Total Daily Energy Expenditure) and objective
2. **Given** a user's objective is "hypertrophy" (muscle gain), **When** macros are calculated, **Then** protein is set to 1.6-2.2g per kg bodyweight, and total calories are TDEE + 10-20% surplus
3. **Given** a user's objective is "definition" (fat loss), **When** macros are calculated, **Then** protein is set to 2.0-2.4g per kg bodyweight (muscle preservation), and total calories are TDEE - 15-25% deficit
4. **Given** a user updates their weight in the profile, **When** they return to the nutrition module, **Then** macro recommendations automatically recalculate based on the new weight
5. **Given** any user views nutrition recommendations, **When** the macros are displayed, **Then** they include a disclaimer: "These are general guidelines. Consult a registered dietitian for personalized nutrition advice."

---

### User Story 4 - Technical Consultation Chat (Priority: P4)

A user asks questions about exercise technique, equipment substitutions, or training concepts via a chat interface and receives evidence-based answers with beginner-friendly explanations.

**Why this priority**: Enhances user experience and education but is not critical for core functionality. Users can train with plans even without this feature.

**Independent Test**: Can be tested by submitting common questions (e.g., "How do I do a proper squat?" or "No cable machine, what can I use?") and verifying responses are clear, accurate, and cite scientific principles.

**Acceptance Scenarios**:

1. **Given** a user is viewing their workout plan, **When** they click on an exercise name, **Then** they can access a chat interface to ask technique questions
2. **Given** a user asks "How do I perform a proper squat?", **When** the AI responds, **Then** the answer includes step-by-step instructions (max 20 words per sentence), common mistakes to avoid, and visual cues
3. **Given** a user asks "I don't have a cable machine for lat pulldowns, what can I do?", **When** the AI responds, **Then** it suggests evidence-based alternatives (e.g., pull-ups, dumbbell rows) with rationale
4. **Given** a user asks about a training concept (e.g., "What is progressive overload?"), **When** the AI responds, **Then** the explanation is in simple language and references scientific principles (e.g., "gradually increasing weight/reps over time to force muscle adaptation")
5. **Given** a user asks a question that requires medical diagnosis, **When** the AI detects this (e.g., "Why does my knee crack during squats?"), **Then** it refuses to diagnose and recommends consulting a healthcare professional

---

### Edge Cases

- **What happens when a user has pre-existing injuries?** System prompts for injury disclosure during onboarding and excludes contraindicated exercises. Medical disclaimer emphasizes consultation with doctor.
- **What happens if a user selects conflicting goals?** (e.g., "strength + definition simultaneously") System explains trade-offs and recommends focusing on one primary goal or suggests "recomposition" as a moderate approach.
- **What happens when a user has no equipment?** System generates bodyweight-only routines with clear progressions (e.g., regular push-ups → diamond push-ups → one-arm progressions).
- **What happens if a user skips multiple workouts?** System detects inactivity, sends a motivational prompt, and offers to regenerate the plan with reduced volume for gradual return.
- **What happens when RPE/pain data is inconsistent?** (e.g., user reports RPE 10 but no pain, then next day RPE 2) System flags anomaly and asks user to verify before making adjustments.

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & User Management
- **FR-000a**: System MUST allow new users to register with email and password (minimum 8 characters, at least one uppercase, one lowercase, one number)
- **FR-000b**: System MUST hash passwords using bcrypt or argon2 before storage (never store plaintext passwords)
- **FR-000c**: System MUST validate email uniqueness during registration and return clear error if email already exists
- **FR-000d**: System MUST issue JWT access tokens (expiry: 24 hours) and refresh tokens (expiry: 30 days) upon successful login
- **FR-000e**: System MUST validate JWT tokens on all protected endpoints and return 401 Unauthorized if token is invalid/expired
- **FR-000f**: System MUST provide password reset flow: request reset via email → receive token → set new password
- **FR-000g**: System MUST implement rate limiting on authentication endpoints (max 5 failed login attempts per email per 15 minutes)
- **FR-000h**: System MUST allow users to delete their account, which permanently removes all associated data (GDPR Right to Erasure)

#### User Profile Management
- **FR-001**: System MUST collect user profile data including age, weight, fitness objective (hypertrophy/volume, definition, strength, recomposition), experience level (beginner, intermediate, advanced), and available training days per week
- **FR-002**: System MUST classify users into fitness levels based on self-reported experience and provide level-appropriate recommendations
- **FR-003**: System MUST allow users to update their profile data (weight, objective, available equipment) at any time
- **FR-004**: System MUST store user profile data as sensitive health information (per Constitution Principle IX - Data Privacy)

#### Workout Plan Generation
- **FR-005**: System MUST generate weekly workout routines based on user objective, experience level, and available equipment
- **FR-006**: System MUST respect evidence-based volume recommendations per muscle group:
  - Beginners: 10-15 sets per muscle group per week
  - Intermediate: 15-20 sets per muscle group per week
  - Advanced: 20-25 sets per muscle group per week
- **FR-007**: System MUST display workout plans in table format showing: exercise name, sets, reps, rest period, and RPE target
- **FR-007a**: System MUST generate workout plans that conform to the following JSON schema with mandatory fields:
  ```json
  {
    "workout_plan": [
      {
        "musculo": "string (required) - Target muscle group (e.g., 'Pectorales', 'Cuádriceps')",
        "ejercicio": "string (required) - Exercise name (e.g., 'Press Banca', 'Sentadilla')",
        "series": "integer (required) - Number of sets (e.g., 3)",
        "repeticiones": "string (required) - Rep range (e.g., '8-12', '6-8')",
        "rpe_objetivo": "integer (required) - Target RPE 1-10 scale (e.g., 7)",
        "descanso_segundos": "integer (required) - Rest period in seconds (e.g., 90)",
        "notas_seguridad": "string (required) - Safety cues and warnings (e.g., 'Mantén espalda recta. Detente si sientes dolor en rodillas.')"
      }
    ],
    "disclaimer_medico": "string (required) - Medical disclaimer text"
  }
  ```
- **FR-007b**: System MUST validate that all generated workout plans include the mandatory fields: `musculo`, `series`, `repeticiones`, `rpe_objetivo`, `notas_seguridad`
- **FR-008**: System MUST include a medical disclaimer on every workout plan stating: "Consult with a healthcare professional before starting any exercise program. Stop immediately if you experience pain."
- **FR-009**: System MUST base all training recommendations on recognized sports science principles (progressive overload, periodization, specificity)
- **FR-009a**: System MUST implement load progression logic based on historical RPE and Fatigue Score:
  - **Progressive Overload Formula**: `New Load = Previous Load × (1 + Progression Factor)`
  - **Progression Factor Calculation**:
    - If Average RPE (last 2 weeks) < 6 AND Fatigue Score < 40: Progression Factor = 0.05 to 0.10 (5-10% increase)
    - If Average RPE (last 2 weeks) = 6-8 AND Fatigue Score 40-60: Progression Factor = 0.02 to 0.05 (2-5% increase)
    - If Average RPE (last 2 weeks) > 8 OR Fatigue Score > 60: Progression Factor = 0 (maintain current load)
    - If Fatigue Score > 80: Progression Factor = -0.20 to -0.30 (20-30% reduction - deload)
  - This formula MUST be passed to the LLM as a system constraint in the workout generation prompt

#### Fatigue Management & Safety
- **FR-010**: System MUST allow users to log post-workout data: RPE (1-10 scale) and pain/discomfort (yes/no + location)
- **FR-011**: System MUST automatically adjust next session intensity based on logged RPE and pain data
- **FR-012**: System MUST reduce volume by 20-30% when user logs RPE 9-10 or reports joint pain
- **FR-013**: System MUST suggest deload week (50% volume reduction) when user reports high fatigue (RPE 8+) for 3+ consecutive sessions
- **FR-014**: System MUST deny high-intensity workout generation and recommend medical consultation when user reports chronic fatigue or persistent joint pain
- **FR-015**: System MUST increase volume/intensity by 5-10% (progressive overload) when user consistently logs low RPE (3-5) for 2+ weeks
- **FR-016**: System MUST exclude exercises that stress injured body parts when user reports pain in specific areas
- **FR-017a**: System MUST calculate a Fatigue Score (0-100) based on historical RPE data, sleep quality (if available), and training volume trends
- **FR-017b**: System MUST apply the following Fatigue Management Rules when generating workout plans:

| Fatigue Score Range | Action | Volume Adjustment | Intensity Adjustment |
|---------------------|--------|-------------------|---------------------|
| **> 80 (High Fatigue)** | Reduce volume, recommend rest | -30% sets/reps | Maintain or reduce RPE target by 1-2 points |
| **60-80 (Moderate Fatigue)** | Reduce volume slightly | -15% sets/reps | Maintain RPE target |
| **40-60 (Normal)** | Maintain current volume | No change | Maintain RPE target |
| **< 40 (Low Fatigue, Recovered)** | Increase intensity/volume | +5-10% sets/reps OR +1 RPE | Progressive overload applied |

- **FR-017c**: System MUST pass the calculated Fatigue Score to the LLM prompt as a context variable for workout generation

#### Nutrition Calculator
- **FR-018**: System MUST calculate Total Daily Energy Expenditure (TDEE) based on user weight, age, activity level
- **FR-019**: System MUST calculate macro targets (protein, carbs, fats in grams) based on TDEE and fitness objective:
  - Hypertrophy: TDEE + 10-20% surplus, 1.6-2.2g protein/kg bodyweight
  - Definition: TDEE - 15-25% deficit, 2.0-2.4g protein/kg bodyweight
  - Strength: TDEE + 5-10% surplus, 1.8-2.0g protein/kg bodyweight
  - Recomposition: TDEE maintenance, 2.0-2.2g protein/kg bodyweight
- **FR-020**: System MUST automatically recalculate macro recommendations when user updates their weight
- **FR-021**: System MUST display nutrition recommendations with disclaimer: "These are general guidelines. Consult a registered dietitian for personalized nutrition advice."

#### Technical Consultation Chat
- **FR-022**: System MUST provide a chat interface for users to ask questions about exercise technique, equipment substitutions, and training concepts
- **FR-023**: System MUST respond to technique questions with step-by-step instructions (max 20 words per sentence), common mistakes, and visual cues
- **FR-024**: System MUST suggest evidence-based equipment alternatives when user asks about substitutions
- **FR-025**: System MUST explain training concepts in simple language with references to scientific principles
- **FR-026**: System MUST refuse to provide medical diagnosis and recommend healthcare consultation when questions require medical expertise
- **FR-027**: Chat responses MUST be beginner-friendly, avoiding unnecessary jargon (per Constitution Principle X - Technical Clarity)

### Key Entities

- **User**: Represents authentication and account identity including email (unique), hashed password (bcrypt/argon2), created_at timestamp, last_login timestamp, email_verified status, password_reset_token (nullable). One-to-one relationship with UserProfile.
- **UserProfile**: Represents a user's fitness identity including user_id (FK to User), age, weight, height, fitness objective (hypertrophy/definition/strength/recomposition), experience level (beginner/intermediate/advanced), available training days per week, equipment access, injury history
- **WorkoutPlan**: Represents a structured training routine including user_id (FK), target muscle groups, exercise selection, volume prescription (sets × reps), intensity targets (RPE), rest periods, weekly structure (training days)
- **Exercise**: Represents a specific movement including name, muscle groups targeted, equipment required, difficulty level, technique cues, contraindications (injuries that exclude this exercise)
- **WorkoutLog**: Represents post-training data including user_id (FK), workout date, completed exercises, logged RPE (1-10 scale), pain indicators (yes/no + location/description), subjective recovery quality
- **NutritionPlan**: Represents dietary recommendations including user_id (FK), calculated TDEE, macro targets (protein/carbs/fats in grams and percentages), caloric adjustment (surplus/deficit), update frequency (recalculates when weight changes)
- **ChatSession**: Represents a consultation interaction including user_id (FK), user question, AI response, question category (technique/equipment/concept), timestamp, response includes scientific references

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete profile setup and receive their first personalized workout plan within 5 minutes of starting the application
- **SC-002**: 90% of generated workout plans respect evidence-based volume guidelines (10-25 sets per muscle group based on user level)
- **SC-003**: System successfully detects and responds to high fatigue/pain indicators in 100% of cases (reduces volume when RPE 9-10 or pain reported)
- **SC-004**: Nutrition macro calculations update within 2 seconds when user weight changes
- **SC-005**: Technical consultation chat provides responses within 10 seconds that are accurate (scientifically grounded) and beginner-friendly (readable at 8th-grade level)
- **SC-006**: Zero instances of the system recommending high-intensity training when user reports chronic fatigue or joint pain (100% safety compliance)
- **SC-007**: All workout plans and nutrition recommendations include required medical/professional disclaimers (100% compliance)
- **SC-008**: Users can understand exercise instructions without external resources (target: 85% of users complete first workout without needing to search for technique videos)

## Technical Constraints

### Backend
- **Framework**: Python 3.11+ with FastAPI for REST API development
- **Validation Layer**: Pydantic v2 for data validation and schema enforcement (native FastAPI integration)
- **Async Runtime**: asyncio for non-blocking LLM API calls and concurrent request handling
- **API Documentation**: OpenAPI 3.0 (auto-generated by FastAPI) for endpoint documentation
- **Python Version**: Minimum Python 3.11 for performance improvements and modern type hints
- **Authentication**: JWT tokens (HS256 algorithm) for stateless authentication. Access tokens expire in 24h, refresh tokens in 30 days. Password hashing via bcrypt (cost factor 12) or argon2id.
- **Database**: PostgreSQL 15+ for relational data persistence with ACID compliance
- **ORM**: SQLAlchemy 2.0+ (async mode) for database abstraction and query building
- **Migrations**: Alembic for database schema version control and migrations
- **Connection Pool**: asyncpg driver for high-performance async PostgreSQL connections

### Frontend
- **Framework**: React 18+ with Vite 5+ as build tool
- **Language**: JavaScript (TypeScript optional but recommended for type safety with API contracts)
- **State Management**: React Context API for global state (user auth, profile). Consider Zustand or Redux Toolkit if complexity grows.
- **Styling**: CSS Modules or Tailwind CSS (aligned with Constitution Principle III - start simple, grow as needed)
- **HTTP Client**: Axios or native fetch for API calls with JWT token injection
- **Routing**: React Router v6 for SPA navigation
- **Build Output**: SPA (Single Page Application) served as static files

## Assumptions

1. **User Honesty**: Users will provide accurate data about their fitness level, weight, and RPE/pain indicators. System design assumes good faith but includes anomaly detection for inconsistent reporting.
2. **LLM Availability**: Anthropic Claude API is available with sufficient rate limits (assumed: 4000 requests/minute for tier 2+ accounts) for generating workout plans, processing chat queries, and providing personalized recommendations. Constitutional AI features ensure safety-first responses aligned with medical disclaimer requirements.
3. **Standard Equipment Categories**: "Available equipment" will be categorized as: None (bodyweight), Basic (dumbbells/resistance bands), Intermediate (barbell/bench), Full Gym (cables/machines/free weights).
4. **TDEE Calculation Method**: Using Mifflin-St Jeor equation for BMR (Basal Metabolic Rate) × activity multiplier (1.2-1.9 based on training frequency).
5. **Progressive Overload Timing**: Automatic intensity increases will be suggested after 2 weeks of consistent low RPE to balance progression with adequate adaptation time.
6. **Data Storage**: User health data (weight, RPE, pain logs) will be stored in PostgreSQL database on the backend server with encryption at rest. Database backups performed daily with 30-day retention. Users have right to data export (JSON format) and permanent deletion (per Constitution Principle IX - GDPR compliance).
7. **Language**: Primary language is Spanish for user-facing content, with English as secondary option.
8. **Medical Disclaimer Sufficiency**: Standard medical disclaimers meet legal requirements for the target deployment region (Spain/Latin America assumed - verify with legal counsel).

## Dependencies

### Backend Dependencies
- **Anthropic Claude API**: Primary LLM provider for workout plan generation and technical consultation chat. Requires API key and handles structured outputs natively via tool use. Expected latency: 2-5 seconds per request. Pricing: ~$3-15 per 1M tokens depending on model (Claude 3.5 Sonnet recommended for balance of cost/performance). Python SDK: `anthropic` package.
- **FastAPI Framework**: Modern async Python web framework with native Pydantic support. Version 0.104.0+.
- **PostgreSQL Database**: Version 15+ with JSONB support for flexible data storage. ACID-compliant for health data integrity.
- **SQLAlchemy ORM**: Version 2.0+ with async support via asyncpg driver.
- **Alembic**: Database migration tool for SQLAlchemy.
- **Python Database Drivers**: `asyncpg` (async PostgreSQL driver), `psycopg2-binary` (sync fallback if needed).
- **Exercise Database**: Requires a structured library of exercises with metadata (muscle groups, equipment, difficulty, technique descriptions, contraindications). Can be seeded into PostgreSQL or loaded from JSON/CSV.
- **Scientific Guidelines**: Recommendations must align with research from recognized bodies (NSCA, ACSM) and cited studies on hypertrophy/strength training
- **Fatigue Model (ML)**: Optional machine learning model for fatigue score prediction; if unavailable, fallback to rule-based calculation

### Frontend Dependencies
- **React**: UI library version 18+
- **Vite**: Build tool and dev server version 5+
- **React Router**: Client-side routing version 6+
- **HTTP Client**: Axios or native fetch API
- **Node.js**: Version 18+ for development and build process

---

## Technical Deep Dive

### 1. LLM Response Schema (Pydantic)

The LLM MUST return workout plans conforming to this Pydantic schema. This ensures type safety, validation, and consistent data structure for the frontend.

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ExerciseBlock(BaseModel):
    """Represents a single exercise in the workout plan."""

    musculo: str = Field(
        ...,
        description="Target muscle group (e.g., 'Pectorales', 'Cuádriceps', 'Dorsales')",
        min_length=3,
        max_length=50
    )

    ejercicio: str = Field(
        ...,
        description="Exercise name (e.g., 'Press Banca', 'Sentadilla', 'Peso Muerto')",
        min_length=3,
        max_length=100
    )

    series: int = Field(
        ...,
        description="Number of sets to perform",
        ge=1,
        le=10
    )

    repeticiones: str = Field(
        ...,
        description="Rep range (e.g., '8-12', '6-8', '15-20')",
        regex=r"^\d{1,2}(-\d{1,2})?$"
    )

    rpe_objetivo: int = Field(
        ...,
        description="Target RPE (Rate of Perceived Exertion) on 1-10 scale",
        ge=1,
        le=10
    )

    descanso_segundos: int = Field(
        ...,
        description="Rest period between sets in seconds",
        ge=30,
        le=600
    )

    notas_seguridad: str = Field(
        ...,
        description="Safety cues, form tips, and warnings (beginner-friendly language)",
        min_length=10,
        max_length=500
    )

    @validator("notas_seguridad")
    def validate_safety_notes(cls, v):
        """Ensure safety notes include critical warnings."""
        required_keywords = ["espalda", "dolor", "detente", "postura", "mantén"]
        if not any(keyword in v.lower() for keyword in required_keywords):
            raise ValueError(
                "Safety notes must include at least one critical safety keyword "
                "(espalda, dolor, detente, postura, mantén)"
            )
        return v


class WorkoutPlan(BaseModel):
    """Complete workout plan with exercises and metadata."""

    workout_plan: List[ExerciseBlock] = Field(
        ...,
        description="List of exercises for the workout session",
        min_items=3,
        max_items=15
    )

    disclaimer_medico: str = Field(
        default="Consulta con un profesional de la salud antes de iniciar cualquier programa de ejercicio. Detente inmediatamente si experimentas dolor.",
        description="Medical disclaimer (auto-generated if not provided)"
    )

    fatiga_score_usado: int = Field(
        ...,
        description="Fatigue score (0-100) used to generate this plan",
        ge=0,
        le=100
    )

    ajuste_aplicado: Optional[str] = Field(
        None,
        description="Explanation of volume/intensity adjustments made (e.g., 'Volumen reducido 30% por fatiga alta')"
    )

    @validator("workout_plan")
    def validate_muscle_distribution(cls, v):
        """Ensure balanced muscle group distribution."""
        muscle_groups = [exercise.musculo for exercise in v]
        if len(set(muscle_groups)) < 2:
            raise ValueError(
                "Workout plan must target at least 2 different muscle groups for balanced training"
            )
        return v
```

**Validation Rules:**
- All fields marked `...` are **required** (cannot be null)
- `series`: Must be between 1-10 sets
- `rpe_objetivo`: Must be between 1-10 (RPE scale)
- `repeticiones`: Must match format "X" or "X-Y" (e.g., "8", "8-12")
- `notas_seguridad`: Must be at least 10 characters and include safety-related keywords
- `workout_plan`: Must contain 3-15 exercises targeting at least 2 muscle groups

---

### 2. Prompt Architecture: Fatigue Score Integration

**Goal**: Pass the ML-computed Fatigue Score to the LLM so it can generate contextually appropriate workout plans.

#### System Prompt Template

```python
SYSTEM_PROMPT_TEMPLATE = """
You are an evidence-based sports coach AI. Your role is to generate safe, scientifically-grounded workout plans.

**USER PROFILE:**
- Objective: {user_objective}
- Experience Level: {experience_level}
- Available Equipment: {equipment}
- Available Days/Week: {days_per_week}

**FATIGUE ANALYSIS (ML Model Output):**
- Current Fatigue Score: {fatigue_score}/100
- Fatigue Category: {fatigue_category}
- Recommended Action: {recommended_action}

**VOLUME ADJUSTMENT RULES (MANDATORY):**
- Fatiga > 80: Reducir volumen 30%, RPE objetivo -2 puntos
- Fatiga 60-80: Reducir volumen 15%, mantener RPE
- Fatiga 40-60: Mantener volumen actual, mantener RPE
- Fatiga < 40: Aumentar volumen 5-10% O aumentar RPE +1 punto (progresión)

**LOAD PROGRESSION FORMULA:**
- Average RPE (last 2 weeks): {avg_rpe_history}
- Progression Factor: {progression_factor}
- Apply: New Load = Previous Load × (1 + {progression_factor})

**RESPONSE FORMAT:**
You MUST respond with a valid JSON object matching the WorkoutPlan Pydantic schema.
All fields (musculo, ejercicio, series, repeticiones, rpe_objetivo, descanso_segundos, notas_seguridad) are REQUIRED.

**SAFETY REQUIREMENTS (NON-NEGOTIABLE):**
1. Include medical disclaimer in every plan
2. If user reports pain or Fatiga > 80, recommend medical consultation
3. Safety notes MUST be beginner-friendly (max 20 words/sentence)
4. NEVER suggest exercises if user reports injury to target muscle group

**SCIENTIFIC BASIS:**
- Use progressive overload principles
- Respect evidence-based volume landmarks (10-25 sets/muscle/week)
- Base recommendations on NSCA/ACSM guidelines

Generate a workout plan for today's training session.
"""

def build_llm_prompt(user_profile, fatigue_data, workout_history):
    """Construct the prompt with fatigue score and progression data."""

    # Calculate progression factor from history
    avg_rpe = calculate_avg_rpe(workout_history, weeks=2)
    progression_factor = calculate_progression_factor(
        avg_rpe=avg_rpe,
        fatigue_score=fatigue_data["score"]
    )

    # Map fatigue score to category and action
    fatigue_category, recommended_action = map_fatigue_category(fatigue_data["score"])

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        user_objective=user_profile.objective,
        experience_level=user_profile.experience_level,
        equipment=", ".join(user_profile.equipment),
        days_per_week=user_profile.days_per_week,
        fatigue_score=fatigue_data["score"],
        fatigue_category=fatigue_category,
        recommended_action=recommended_action,
        avg_rpe_history=avg_rpe,
        progression_factor=progression_factor
    )

    return prompt


def map_fatigue_category(score: int) -> tuple[str, str]:
    """Map fatigue score to human-readable category and action."""
    if score > 80:
        return ("ALTA FATIGA", "Reducir volumen 30%, considerar día de descanso")
    elif score > 60:
        return ("FATIGA MODERADA", "Reducir volumen 15%, mantener intensidad")
    elif score > 40:
        return ("FATIGA NORMAL", "Mantener volumen e intensidad actuales")
    else:
        return ("RECUPERADO", "Aplicar progresión: aumentar volumen o intensidad")
```

#### Data Flow Diagram

```
┌─────────────────────┐
│  User Workout Log   │
│  (RPE, Pain, Date)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│   ML Fatigue Model          │◄─── Optional: Sleep data, HRV, etc.
│   (Predicts 0-100 score)    │
└──────────┬──────────────────┘
           │
           │ Fatigue Score: 75
           │
           ▼
┌─────────────────────────────┐
│   Prompt Builder            │
│   - Inject fatigue score    │
│   - Calculate progression   │
│   - Apply adjustment rules  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   LLM API Call              │
│   (Anthropic/OpenAI)        │
│   + Pydantic schema         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   Validate Response         │
│   (Pydantic parsing)        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   Display to User           │
│   (Table format + safety)   │
└─────────────────────────────┘
```

---

### 3. Error Handling & Fallback Strategy

**Failure Modes and Mitigation:**

#### 3.1 ML Fatigue Model Failure

**Scenario**: ML model unavailable, returns error, or takes >5 seconds to respond.

**Fallback Strategy**: Use rule-based fatigue score calculation.

```python
def calculate_fatigue_score_fallback(workout_history: List[WorkoutLog]) -> dict:
    """
    Rule-based fatigue calculation when ML model fails.
    Based on simple heuristics from recent workout logs.
    """

    # Get last 7 days of workouts
    recent_workouts = get_recent_workouts(workout_history, days=7)

    if not recent_workouts:
        return {
            "score": 50,  # Neutral baseline
            "source": "fallback_no_history",
            "confidence": "low"
        }

    # Calculate average RPE from recent sessions
    avg_rpe = sum(w.rpe for w in recent_workouts) / len(recent_workouts)

    # Check for pain reports
    pain_count = sum(1 for w in recent_workouts if w.pain_reported)

    # Calculate training frequency (sessions per week)
    sessions_per_week = len(recent_workouts)

    # Heuristic formula
    base_fatigue = (avg_rpe / 10) * 100  # RPE 8/10 = 80 fatigue
    pain_penalty = pain_count * 15  # Each pain report adds 15 points
    frequency_factor = max(0, (sessions_per_week - 4) * 10)  # Penalty for >4 sessions/week

    fatigue_score = min(100, base_fatigue + pain_penalty + frequency_factor)

    return {
        "score": int(fatigue_score),
        "source": "fallback_rule_based",
        "confidence": "medium",
        "avg_rpe": avg_rpe,
        "pain_reports": pain_count,
        "sessions_per_week": sessions_per_week
    }


def get_fatigue_score(workout_history: List[WorkoutLog], ml_model=None) -> dict:
    """
    Primary fatigue score retrieval with automatic fallback.
    """

    # Try ML model first (if available)
    if ml_model is not None:
        try:
            result = ml_model.predict(workout_history, timeout=5)
            return {
                "score": result["fatigue_score"],
                "source": "ml_model",
                "confidence": result.get("confidence", "high"),
                "model_version": ml_model.version
            }
        except (TimeoutError, ModelError, ConnectionError) as e:
            logger.warning(f"ML model failed: {e}. Falling back to rule-based calculation.")

    # Fallback to rule-based
    return calculate_fatigue_score_fallback(workout_history)
```

**Fallback Decision Tree:**

```
┌─────────────────────────────┐
│  Request Fatigue Score      │
└──────────┬──────────────────┘
           │
           ▼
     ┌─────────────┐
     │ ML Model    │
     │ Available?  │
     └──┬─────┬────┘
        │     │
      Yes     No
        │     │
        ▼     └──────────────┐
   ┌─────────────┐           │
   │ Call ML API │           │
   └──┬──────────┘           │
      │                      │
      ▼                      │
   Success?                  │
   ┌──┴──┐                   │
  Yes   No                   │
   │     │                   │
   │     └───────────────────┤
   │                         │
   ▼                         ▼
┌────────────┐      ┌──────────────────┐
│ Use ML     │      │ Fallback:        │
│ Score      │      │ Rule-Based Calc  │
└────────────┘      └──────────────────┘
                     (avg_rpe + pain + frequency)
```

#### 3.2 LLM API Failure

**Scenario**: LLM API unavailable, returns invalid JSON, or violates Pydantic schema.

**Mitigation:**

1. **Retry Logic**: Retry API call up to 3 times with exponential backoff (1s, 2s, 4s)
2. **Schema Validation**: Use Pydantic to validate response; if validation fails, log error and retry
3. **Fallback Plan**: If all retries fail, generate a **template-based workout** from predefined exercise library

```python
def generate_workout_with_fallback(
    user_profile,
    fatigue_score,
    llm_client,
    max_retries=3
) -> WorkoutPlan:
    """Generate workout plan with automatic fallback."""

    for attempt in range(max_retries):
        try:
            # Build prompt with fatigue score
            prompt = build_llm_prompt(user_profile, fatigue_score)

            # Call LLM API
            response = llm_client.generate(
                prompt=prompt,
                response_format=WorkoutPlan,  # Pydantic schema
                timeout=30
            )

            # Validate response
            workout_plan = WorkoutPlan.parse_obj(response)
            logger.info(f"LLM workout generation successful (attempt {attempt + 1})")
            return workout_plan

        except (APIError, ValidationError, TimeoutError) as e:
            logger.warning(f"LLM generation failed (attempt {attempt + 1}): {e}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                logger.error("All LLM retries exhausted. Using template fallback.")
                return generate_template_workout(user_profile, fatigue_score)


def generate_template_workout(user_profile, fatigue_score) -> WorkoutPlan:
    """
    Generate a safe, template-based workout when LLM fails.
    Uses predefined exercise library filtered by user profile.
    """

    # Load exercises from database
    exercises = load_exercise_library(
        objective=user_profile.objective,
        experience=user_profile.experience_level,
        equipment=user_profile.equipment
    )

    # Apply fatigue adjustments to volume
    base_sets = 3
    if fatigue_score > 80:
        adjusted_sets = 2  # Reduce 30%
    elif fatigue_score > 60:
        adjusted_sets = 3  # Maintain
    else:
        adjusted_sets = 4  # Increase for progression

    # Build workout blocks
    workout_blocks = []
    for exercise in exercises[:6]:  # Limit to 6 exercises
        workout_blocks.append(
            ExerciseBlock(
                musculo=exercise.muscle_group,
                ejercicio=exercise.name,
                series=adjusted_sets,
                repeticiones=exercise.rep_range,
                rpe_objetivo=7,  # Conservative RPE
                descanso_segundos=exercise.rest_period,
                notas_seguridad=exercise.safety_notes
            )
        )

    return WorkoutPlan(
        workout_plan=workout_blocks,
        fatiga_score_usado=fatigue_score,
        ajuste_aplicado=f"Plan generado por plantilla (fallback). Fatiga: {fatigue_score}"
    )
```

#### 3.3 Invalid User Input

**Scenario**: User enters invalid RPE (e.g., RPE 15), missing data, or contradictory information.

**Mitigation:**
- **Frontend Validation**: Use HTML5 input constraints and JavaScript validation before submission
- **Backend Validation**: Pydantic models for all user inputs with clear error messages
- **Graceful Degradation**: If RPE missing, use last known value or default to neutral (RPE 7)

```python
class WorkoutLogInput(BaseModel):
    """User input validation for workout logs."""

    rpe: int = Field(..., ge=1, le=10, description="Rate of Perceived Exertion (1-10)")
    pain_reported: bool = Field(default=False)
    pain_location: Optional[str] = Field(None, max_length=200)

    @validator("pain_location")
    def validate_pain_location(cls, v, values):
        """Pain location required if pain_reported is True."""
        if values.get("pain_reported") and not v:
            raise ValueError("pain_location required when pain_reported is True")
        return v
```

---

### 4. Testing & Validation Strategy

**Stress Test Scenarios:**

1. **High Fatigue Edge Case**: User with Fatiga Score = 95 should receive volume reduced by 30%, RPE reduced, and medical consultation warning
2. **ML Model Outage**: Simulate ML model failure; verify fallback produces valid fatigue score within 500ms
3. **LLM Hallucination**: Inject malformed LLM response; verify Pydantic validation catches error and triggers retry/fallback
4. **Schema Violation**: LLM returns workout missing `notas_seguridad`; verify validation fails and error is logged
5. **Progressive Overload Logic**: User with 2 weeks of RPE 4-5 and Fatiga Score 30 should receive +10% volume increase

**Validation Checklist:**
- ✅ All LLM responses pass Pydantic validation
- ✅ Fatigue scores always between 0-100
- ✅ Volume adjustments match fatigue rules table
- ✅ Medical disclaimers present in 100% of plans
- ✅ Fallback systems activate within 5 seconds of primary failure
- ✅ No exercise recommended for injured body parts

## Clarifications

### Session 2026-02-18

- Q: Which LLM provider should be used for workout generation and chat functionality? (Affects costs, latency, deployment strategy) → A: Anthropic Claude (API Cloud)
- Q: Which backend framework should be used for API development? (Affects development velocity, Pydantic integration, async capabilities) → A: Python + FastAPI
- Q: How should users authenticate and be identified in the system? (Affects data model, security architecture, privacy compliance) → A: Email/Password + JWT tokens
- Q: Which frontend framework should be used for the web UI? (Affects team skills, component reusability, development velocity) → A: React + Vite
- Q: Which database technology should be used for data persistence? (Affects data integrity, query capabilities, scalability, deployment) → A: PostgreSQL

## Out of Scope (Explicitly Excluded)

- **Workout Video Demonstrations**: MVP will not include video content; text-based technique cues only (videos can be added in future iterations)
- **Social Features**: No community, sharing, or social networking functionality in MVP
- **Wearable Integration**: No direct integration with fitness trackers or smartwatches (users manually log RPE/pain)
- **Progress Photos**: No photo upload or visual progress tracking in MVP
- **Supplements Recommendations**: System will not recommend supplements (per Constitution Principle VIII - only evidence-based training/nutrition)
- **Custom Exercise Creation**: Users cannot add custom exercises; limited to predefined exercise library
- **Multi-Language Support**: MVP focuses on Spanish only; English can be added post-launch
