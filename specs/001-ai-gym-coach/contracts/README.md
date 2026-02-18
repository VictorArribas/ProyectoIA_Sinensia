# API Contracts: Smart AI Gym Coach (SAIGC)

**Feature**: 001-ai-gym-coach
**Date**: 2026-02-18
**Format**: OpenAPI 3.0 (YAML)

## Overview

This directory contains OpenAPI 3.0 specifications for all REST API endpoints. These contracts define:
- Request/response schemas (Pydantic models converted to JSON Schema)
- Authentication requirements (JWT Bearer tokens)
- Validation rules
- Error responses

## Contract Files

### 1. auth.yaml - Authentication Endpoints

**Base Path**: `/api/v1/auth`

**Endpoints**:
- `POST /register` - Create new user account (email + password)
- `POST /login` - Authenticate and receive JWT tokens
- `POST /refresh` - Refresh access token using refresh token
- `POST /logout` - Invalidate refresh token
- `POST /password-reset/request` - Request password reset email
- `POST /password-reset/confirm` - Confirm password reset with token

### 2. workouts.yaml - Workout Generation & History

**Base Path**: `/api/v1/workouts`

**Endpoints**:
- `POST /generate` - Generate new workout plan (calls Anthropic Claude LLM)
  - Request: `{ user_profile_id, fatigue_score }`
  - Response: `WorkoutPlan` schema (Pydantic)
- `GET /history` - Get past workout plans (paginated)
- `GET /{workout_plan_id}` - Get specific workout plan
- `DELETE /{workout_plan_id}` - Delete workout plan

**Authentication**: Requires valid JWT access token

### 3. fatigue.yaml - Fatigue Logging & Scoring

**Base Path**: `/api/v1/fatigue`

**Endpoints**:
- `POST /logs` - Log post-workout RPE and pain
  - Request: `{ rpe: int (1-10), pain_reported: bool, pain_location: str }`
  - Response: `WorkoutLog` schema
- `GET /logs` - Get workout log history (last 30 days)
- `GET /score` - Get current fatigue score (0-100)
  - Response: `{ score: int, source: "ml_model"|"rule_based", confidence: "high"|"medium"|"low" }`
- `GET /score/history` - Get fatigue trend (last 14 days for chart)

**Authentication**: Requires valid JWT access token

### 4. nutrition.yaml - Nutrition Calculator

**Base Path**: `/api/v1/nutrition`

**Endpoints**:
- `GET /calculate` - Calculate TDEE and macros based on current user profile
  - Response: `NutritionPlan` schema (tdee, protein_g, carbs_g, fat_g)
- `PUT /recalculate` - Force recalculation after weight update (auto-triggered by profile update)

**Authentication**: Requires valid JWT access token

### 5. chat.yaml - Technical Consultation Chat

**Base Path**: `/api/v1/chat`

**Endpoints**:
- `POST /ask` - Send question to LLM (technique, equipment, concepts)
  - Request: `{ question: str (max 1000 chars) }`
  - Response: `{ response: str, question_category: str, created_at: datetime }`
- `GET /history` - Get past chat sessions (last 30 days)

**Authentication**: Requires valid JWT access token

### 6. profile.yaml - User Profile Management

**Base Path**: `/api/v1/profile`

**Endpoints**:
- `GET /me` - Get current user's profile
- `POST /create` - Create user profile (onboarding after registration)
  - Request: `{ age, weight, height, objective, experience_level, training_days_per_week, equipment, injury_history }`
- `PUT /update` - Update user profile
- `DELETE /delete` - Delete user account and all data (GDPR Right to Erasure)

**Authentication**: Requires valid JWT access token

---

## Common Schemas

### JWTToken (Response)
```yaml
type: object
properties:
  access_token:
    type: string
    description: JWT access token (24h expiry)
  refresh_token:
    type: string
    description: JWT refresh token (30d expiry)
  token_type:
    type: string
    enum: [bearer]
```

### ErrorResponse (4xx, 5xx)
```yaml
type: object
properties:
  detail:
    type: string
    description: Human-readable error message
  error_code:
    type: string
    description: Machine-readable error code
  timestamp:
    type: string
    format: date-time
```

### ExerciseBlock (Pydantic schema from spec.md)
```yaml
type: object
required:
  - musculo
  - ejercicio
  - series
  - repeticiones
  - rpe_objetivo
  - descanso_segundos
  - notas_seguridad
properties:
  musculo:
    type: string
    minLength: 3
    maxLength: 50
  ejercicio:
    type: string
    minLength: 3
    maxLength: 100
  series:
    type: integer
    minimum: 1
    maximum: 10
  repeticiones:
    type: string
    pattern: "^\\d{1,2}(-\\d{1,2})?$"
  rpe_objetivo:
    type: integer
    minimum: 1
    maximum: 10
  descanso_segundos:
    type: integer
    minimum: 30
    maximum: 600
  notas_seguridad:
    type: string
    minLength: 10
    maxLength: 500
```

### WorkoutPlan (Pydantic schema)
```yaml
type: object
required:
  - workout_plan
  - disclaimer_medico
  - fatiga_score_usado
properties:
  workout_plan:
    type: array
    items:
      $ref: '#/components/schemas/ExerciseBlock'
    minItems: 3
    maxItems: 15
  disclaimer_medico:
    type: string
    default: "Consulta con un profesional de la salud antes de iniciar cualquier programa de ejercicio..."
  fatiga_score_usado:
    type: integer
    minimum: 0
    maximum: 100
  ajuste_aplicado:
    type: string
    nullable: true
```

---

## Authentication Flow

All protected endpoints require JWT Bearer token in `Authorization` header:

```http
GET /api/v1/workouts/history
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Expiry**:
- Access token: 24 hours
- Refresh token: 30 days

**Refresh Flow**:
1. Access token expires → API returns `401 Unauthorized`
2. Frontend calls `POST /auth/refresh` with refresh token
3. Receive new access token
4. Retry original request with new token

---

## Rate Limiting

**Authentication endpoints**:
- `POST /auth/login`: 5 requests per 15 minutes per email (FR-000g)
- `POST /auth/register`: 3 requests per hour per IP

**LLM endpoints** (expensive operations):
- `POST /workouts/generate`: 10 requests per hour per user
- `POST /chat/ask`: 20 requests per hour per user

**Standard endpoints**: 100 requests per minute per user

---

## Error Codes

| HTTP Status | error_code | Description |
|-------------|------------|-------------|
| 400 | `VALIDATION_ERROR` | Request body validation failed (Pydantic) |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT token |
| 403 | `FORBIDDEN` | Valid token but insufficient permissions |
| 404 | `NOT_FOUND` | Resource not found (e.g., workout plan ID) |
| 409 | `CONFLICT` | Resource conflict (e.g., email already exists) |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error (LLM API failure, database error) |
| 503 | `SERVICE_UNAVAILABLE` | Anthropic Claude API unavailable |

---

## Implementation Notes

### FastAPI Auto-Generation

FastAPI generates OpenAPI 3.0 specs automatically from Pydantic models:

```python
# src/api/workouts.py
from fastapi import APIRouter, Depends
from src.schemas.workout import WorkoutPlanResponse, WorkoutGenerateRequest

router = APIRouter(prefix="/api/v1/workouts", tags=["workouts"])

@router.post("/generate", response_model=WorkoutPlanResponse)
async def generate_workout(
    request: WorkoutGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate personalized workout plan based on user profile and fatigue score.

    - Calls Anthropic Claude API with user context
    - Applies fatigue adjustments per FR-017b rules
    - Validates response against WorkoutPlan Pydantic schema
    - Returns structured JSON with disclaimer
    """
    return await workout_service.generate(request, current_user)
```

**View generated OpenAPI**: http://localhost:8000/docs

### Contract Testing

```python
# tests/contract/test_workout_contracts.py
def test_generate_workout_response_matches_schema():
    """Ensure /workouts/generate response matches WorkoutPlan schema."""
    response = client.post("/api/v1/workouts/generate", json={...}, headers={...})
    assert response.status_code == 200

    # Validate against Pydantic schema
    workout_plan = WorkoutPlanResponse.parse_obj(response.json())
    assert len(workout_plan.workout_plan) >= 3
    assert workout_plan.fatiga_score_usado >= 0
```

---

**API Contracts Status**: ✅ **DOCUMENTED** - Full OpenAPI 3.0 specs ready for frontend integration and contract testing.

**Next Steps**:
1. FastAPI will auto-generate these specs from Pydantic models
2. Export full OpenAPI YAML: `http://localhost:8000/openapi.json`
3. Generate client SDKs: `openapi-generator-cli generate -i openapi.json -g typescript-axios -o frontend/src/generated`
