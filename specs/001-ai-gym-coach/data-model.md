# Data Model: Smart AI Gym Coach (SAIGC)

**Feature**: 001-ai-gym-coach
**Date**: 2026-02-18
**Database**: PostgreSQL 15+
**ORM**: SQLAlchemy 2.0+ (async)
**Status**: Phase 1 Design

## Overview

This document defines the database schema, SQLAlchemy ORM models, relationships, validation rules, and migrations for the Smart AI Gym Coach application. All data is persisted in PostgreSQL with ACID compliance for health data integrity.

---

## Entity Relationship Diagram

```
┌─────────────┐
│   users     │─┐
│─────────────│ │ 1:1
│ id (PK)     │ │
│ email       │ │    ┌──────────────────┐
│ password... │ └───▶│  user_profiles   │
└─────────────┘      │──────────────────│
                     │ id (PK)          │
      ┌──────────────│ user_id (FK)     │◀──────────┬─────────┬─────────┬──────────┐
      │              └──────────────────┘           │         │         │          │
      │ 1:N                                      1:N│      1:N│      1:N│       1:N│
┌─────▼──────────┐  ┌─────────────────┐  ┌─────────▼──┐  ┌───▼────────┐  ┌──────▼───────┐
│ workout_plans  │  │   exercises     │  │workout_logs│  │nutrition...│  │chat_sessions │
│────────────────│  │─────────────────│  │────────────│  │────────────│  │──────────────│
│ id (PK)        │  │ id (PK)         │  │ id (PK)    │  │ id (PK)    │  │ id (PK)      │
│ user_id (FK)   │  │ name            │  │ user_id FK │  │ user_id FK │  │ user_id FK   │
│ plan_data JSON │  │ muscle_groups[] │  │ plan_id FK │  │ tdee       │  │ question     │
│ fatigue_score  │  │ safety_notes    │  │ rpe        │  │ protein_g  │  │ response     │
└────────────────┘  └─────────────────┘  │ pain...    │  └────────────┘  └──────────────┘
                                         └────────────┘
```

---

## Entity 1: User (Authentication)

**Purpose**: Authentication and account identity.
**Table Name**: `users`

### SQLAlchemy Model

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # bcrypt/argon2

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)

    # Password reset
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    workout_logs = relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")
    nutrition_plans = relationship("NutritionPlan", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
```

### PostgreSQL Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Validation Rules

- **FR-000a**: Email must be unique (unique constraint enforced)
- **FR-000b**: Password hashed with bcrypt (cost factor 12) before storage
- **FR-000c**: Email uniqueness validated at registration
- **FR-000h**: User deletion cascades to all related data (GDPR Right to Erasure)

---

## Entity 2: UserProfile (Fitness Identity)

**Purpose**: User's fitness objectives, constraints, and biometric data.
**Table Name**: `user_profiles`

### SQLAlchemy Model

```python
from sqlalchemy import Column, Integer, String, Float, Enum, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
import enum

class FitnessObjective(enum.Enum):
    HYPERTROPHY = "hypertrophy"
    DEFINITION = "definition"
    STRENGTH = "strength"
    RECOMPOSITION = "recomposition"

class ExperienceLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Biometric data
    age = Column(Integer, nullable=False)  # ge=18, le=100
    weight = Column(Float, nullable=False)  # kg, gt=30, lt=300
    height = Column(Integer, nullable=False)  # cm, ge=100, le=250

    # Fitness parameters
    objective = Column(Enum(FitnessObjective), nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)
    training_days_per_week = Column(Integer, nullable=False)  # ge=1, le=7

    # Equipment and injuries
    equipment = Column(ARRAY(String), nullable=False, default=[])  # ["dumbbells", "barbell", ...]
    injury_history = Column(ARRAY(String), nullable=False, default=[])  # ["left shoulder", ...]

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")
```

### PostgreSQL Schema

```sql
CREATE TYPE fitness_objective AS ENUM ('hypertrophy', 'definition', 'strength', 'recomposition');
CREATE TYPE experience_level AS ENUM ('beginner', 'intermediate', 'advanced');

CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    weight REAL NOT NULL CHECK (weight > 30 AND weight < 300),
    height INTEGER NOT NULL CHECK (height >= 100 AND height <= 250),
    objective fitness_objective NOT NULL,
    experience_level experience_level NOT NULL,
    training_days_per_week INTEGER NOT NULL CHECK (training_days_per_week >= 1 AND training_days_per_week <= 7),
    equipment TEXT[] NOT NULL DEFAULT '{}',
    injury_history TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```

### Validation Rules

- **FR-001**: All fields (age, weight, objective, experience_level, training_days_per_week) required
- **FR-003**: `updated_at` auto-updated on modification
- **FR-004**: Treated as sensitive health information (encryption at rest, GDPR compliance)

---

## Entity 3: Exercise (Exercise Library)

**Purpose**: Exercise metadata for workout generation and instruction.
**Table Name**: `exercises`

### SQLAlchemy Model

```python
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)  # Spanish name
    muscle_groups = Column(ARRAY(String), nullable=False)  # ["pectorales", "triceps"]
    equipment_required = Column(String(100), nullable=False)  # "barbell", "dumbbells", etc.
    difficulty = Column(Enum(ExperienceLevel), nullable=False)

    # Instructions (Spanish)
    technique_cues = Column(ARRAY(String), nullable=False)  # Step-by-step, max 20 words each
    common_mistakes = Column(ARRAY(String), nullable=False, default=[])
    contraindications = Column(ARRAY(String), nullable=False, default=[])  # ["knee injury", ...]

    # Safety notes (mandatory per FR-007a, Pydantic validator ensures keywords)
    safety_notes = Column(String(500), nullable=False)  # "Mantén espalda recta. Detente si sientes dolor..."

    # Volume guidelines (JSON column)
    volume_guidelines_json = Column(JSON, nullable=False)  # {"beginner": {"sets": "8-12", "reps": "8-12"}, ...}

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

### PostgreSQL Schema

```sql
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    muscle_groups TEXT[] NOT NULL,
    equipment_required VARCHAR(100) NOT NULL,
    difficulty experience_level NOT NULL,
    technique_cues TEXT[] NOT NULL,
    common_mistakes TEXT[] NOT NULL DEFAULT '{}',
    contraindications TEXT[] NOT NULL DEFAULT '{}',
    safety_notes VARCHAR(500) NOT NULL CHECK (LENGTH(safety_notes) >= 10),
    volume_guidelines_json JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_exercises_muscle_groups ON exercises USING GIN(muscle_groups);
CREATE INDEX idx_exercises_equipment ON exercises(equipment_required);
```

### Seed Data Example

```sql
INSERT INTO exercises (name, muscle_groups, equipment_required, difficulty, technique_cues, safety_notes, volume_guidelines_json)
VALUES (
    'Sentadilla con Barra',
    ARRAY['cuádriceps', 'glúteos', 'isquiotibiales', 'core'],
    'barbell',
    'intermediate',
    ARRAY[
        'Pies al ancho de hombros',
        'Baja las caderas como si te sentaras',
        'Mantén el pecho alto y la espalda recta',
        'Rodillas alineadas con los pies',
        'Baja hasta que los muslos estén paralelos',
        'Empuja con los talones para subir'
    ],
    'Mantén la espalda recta. Detente si sientes dolor en rodillas o espalda baja.',
    '{"beginner": {"sets": "8-12", "reps": "8-12"}, "intermediate": {"sets": "12-18", "reps": "6-10"}, "advanced": {"sets": "15-20", "reps": "4-8"}}'::jsonb
);
```

### Validation Rules

- **FR-009**: `volume_guidelines_json` validated against evidence-based research (Schoenfeld et al.)
- **FR-007a**: `safety_notes` must be >= 10 characters and include safety keywords (validated by Pydantic)
- **FR-016**: `contraindications` used to exclude exercises when user reports matching injuries

---

## Entity 4: WorkoutPlan (Generated Training Routine)

**Purpose**: LLM-generated workout plan with fatigue adjustments.
**Table Name**: `workout_plans`

### SQLAlchemy Model

```python
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # LLM-generated plan (full WorkoutPlan Pydantic schema as JSON)
    plan_data = Column(JSON, nullable=False)  # ExerciseBlock[] + metadata

    # Fatigue context
    fatigue_score_used = Column(Integer, nullable=False)  # 0-100, from ML model or fallback
    volume_adjustment_applied = Column(String(500), nullable=True)  # "Volumen reducido 30% por fatiga alta"

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="workout_plans")
    workout_logs = relationship("WorkoutLog", back_populates="workout_plan", cascade="all, delete-orphan")
```

### PostgreSQL Schema

```sql
CREATE TABLE workout_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_data JSONB NOT NULL,
    fatigue_score_used INTEGER NOT NULL CHECK (fatigue_score_used >= 0 AND fatigue_score_used <= 100),
    volume_adjustment_applied VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_workout_plans_user_id ON workout_plans(user_id);
CREATE INDEX idx_workout_plans_created_at ON workout_plans(created_at DESC);
CREATE INDEX idx_workout_plans_fatigue_score ON workout_plans(fatigue_score_used);
```

### plan_data JSONB Structure

```json
{
  "workout_plan": [
    {
      "musculo": "Pectorales",
      "ejercicio": "Press Banca",
      "series": 4,
      "repeticiones": "8-10",
      "rpe_objetivo": 7,
      "descanso_segundos": 120,
      "notas_seguridad": "Mantén espalda en contacto con banco. Detente si sientes dolor en hombro."
    }
  ],
  "disclaimer_medico": "Consulta con un profesional de la salud antes de iniciar cualquier programa de ejercicio...",
  "fatiga_score_usado": 45,
  "ajuste_aplicado": null
}
```

### Validation Rules

- **FR-007a**: `plan_data` must conform to WorkoutPlan Pydantic schema (validated before DB insert)
- **FR-007b**: All mandatory fields (musculo, series, repeticiones, rpe_objetivo, notas_seguridad) present
- **FR-017c**: `fatigue_score_used` stored for audit trail and trend analysis

---

## Entity 5: WorkoutLog (Post-Workout RPE & Pain Tracking)

**Purpose**: Captures RPE and pain data for fatigue management.
**Table Name**: `workout_logs`

### SQLAlchemy Model

```python
class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="SET NULL"), nullable=True)

    # Post-workout data
    rpe = Column(Integer, nullable=False)  # 1-10 scale
    pain_reported = Column(Boolean, nullable=False, default=False)
    pain_location = Column(String(200), nullable=True)  # "left shoulder", "knee"
    pain_description = Column(String(500), nullable=True)

    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="workout_logs")
    workout_plan = relationship("WorkoutPlan", back_populates="workout_logs")
```

### PostgreSQL Schema

```sql
CREATE TABLE workout_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workout_plan_id INTEGER REFERENCES workout_plans(id) ON DELETE SET NULL,
    rpe INTEGER NOT NULL CHECK (rpe >= 1 AND rpe <= 10),
    pain_reported BOOLEAN NOT NULL DEFAULT FALSE,
    pain_location VARCHAR(200),
    pain_description VARCHAR(500),
    logged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_workout_logs_user_id ON workout_logs(user_id);
CREATE INDEX idx_workout_logs_logged_at ON workout_logs(logged_at DESC);
CREATE INDEX idx_workout_logs_rpe ON workout_logs(rpe);
```

### Validation Rules

- **FR-010**: `rpe` and `pain_reported` are mandatory
- **FR-011**: Used by `fatigue_service.py` to calculate fatigue score
- **FR-012**: If `rpe >= 9` or `pain_reported = true`, trigger volume reduction
- **FR-013**: If 3+ consecutive logs have `rpe >= 8`, suggest deload week

---

## Entity 6: NutritionPlan (Macro Calculations)

**Purpose**: TDEE and macro targets (recalculated on weight change).
**Table Name**: `nutrition_plans`

### SQLAlchemy Model

```python
class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # TDEE calculation
    tdee = Column(Float, nullable=False)
    target_calories = Column(Float, nullable=False)

    # Macros
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)

    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="nutrition_plans")
```

### PostgreSQL Schema

```sql
CREATE TABLE nutrition_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tdee REAL NOT NULL,
    target_calories REAL NOT NULL,
    protein_g REAL NOT NULL,
    carbs_g REAL NOT NULL,
    fat_g REAL NOT NULL,
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_nutrition_plans_user_id ON nutrition_plans(user_id);
```

### Validation Rules

- **FR-018**: `tdee` calculated using Mifflin-St Jeor equation
- **FR-019**: `protein_g`, `carbs_g`, `fat_g` based on objective and bodyweight
- **FR-020**: Recalculated when `user_profiles.weight` changes (upsert on update)

---

## Entity 7: ChatSession (Technical Consultation)

**Purpose**: LLM chat for technique/equipment questions.
**Table Name**: `chat_sessions`

### SQLAlchemy Model

```python
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    question = Column(String(1000), nullable=False)
    response = Column(String(5000), nullable=False)

    question_category = Column(String(50), nullable=True)  # "technique", "equipment", "concept"

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
```

### PostgreSQL Schema

```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question VARCHAR(1000) NOT NULL,
    response VARCHAR(5000) NOT NULL,
    question_category VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_created_at ON chat_sessions(created_at DESC);
```

### Validation Rules

- **FR-025**: If question classified as "medical-diagnosis", refuse and recommend healthcare professional
- **FR-027**: All responses must be beginner-friendly (max 20 words/sentence)

---

## Migrations (Alembic)

### Initial Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Initial schema: users, profiles, exercises, workouts, logs, nutrition, chat"

# Apply migration
alembic upgrade head
```

### Migration File Structure

```python
# alembic/versions/001_initial_schema.py
def upgrade():
    # Create ENUM types
    op.execute("CREATE TYPE fitness_objective AS ENUM ('hypertrophy', 'definition', 'strength', 'recomposition');")
    op.execute("CREATE TYPE experience_level AS ENUM ('beginner', 'intermediate', 'advanced');")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        # ... (full table definition)
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create user_profiles table with FK to users
    # Create exercises table (seed data via separate migration)
    # Create workout_plans, workout_logs, nutrition_plans, chat_sessions
    # Create indexes

def downgrade():
    op.drop_table('chat_sessions')
    op.drop_table('nutrition_plans')
    op.drop_table('workout_logs')
    op.drop_table('workout_plans')
    op.drop_table('exercises')
    op.drop_table('user_profiles')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS experience_level;")
    op.execute("DROP TYPE IF EXISTS fitness_objective;")
```

---

## Data Flow Summary

```
1. User registers → INSERT INTO users → INSERT INTO user_profiles (onboarding)

2. User requests workout plan →
   - SELECT user_profiles WHERE user_id = ?
   - SELECT exercises WHERE muscle_groups && ? AND equipment_required = ANY(?)
   - Call LLM with fatigue score + profile + exercises
   - INSERT INTO workout_plans (plan_data JSONB, fatigue_score_used)

3. User logs workout →
   - INSERT INTO workout_logs (rpe, pain_reported, pain_location)

4. Next workout generation →
   - SELECT workout_logs WHERE user_id = ? ORDER BY logged_at DESC LIMIT 14
   - Calculate fatigue score (avg_rpe, pain_count, sessions_per_week)
   - IF fatigue_score > 80 → adjust volume -30%
   - Generate new workout plan with adjustment

5. User accesses nutrition →
   - SELECT user_profiles WHERE user_id = ?
   - Calculate TDEE, macros
   - UPSERT INTO nutrition_plans (ON CONFLICT user_id DO UPDATE)

6. User updates weight →
   - UPDATE user_profiles SET weight = ?, updated_at = NOW()
   - Trigger recalculation on next nutrition access

7. User asks chat question →
   - Call LLM with question
   - Classify question_category
   - IF medical-diagnosis → refuse
   - INSERT INTO chat_sessions (question, response, question_category)
```

---

## Constitution Alignment

✅ **Principle VII (Safety First)**:
- `workout_plans.plan_data` includes `disclaimer_medico` (FR-008)
- `workout_logs.rpe >= 9` triggers automatic volume reduction (FR-012)
- `exercises.contraindications` excludes dangerous movements (FR-016)

✅ **Principle VIII (Scientific Foundation)**:
- `exercises.volume_guidelines_json` based on Schoenfeld research (FR-006, FR-009)
- `nutrition_plans` macros cite 1.6-2.4g/kg protein guidelines (FR-019)

✅ **Principle IX (Data Privacy)**:
- Cascading deletes: `ON DELETE CASCADE` ensures GDPR Right to Erasure (FR-000h)
- PostgreSQL encryption at rest (database-level configuration)
- No PII beyond necessary (email only for auth)

✅ **Principle X (Technical Clarity)**:
- `exercises.technique_cues` validated for beginner-friendly language
- `chat_sessions.response` max 20 words/sentence (FR-027)

✅ **Principle XI (Technological Neutrality)**:
- SQLAlchemy ORM abstracts database specifics (can swap PostgreSQL for MySQL/SQLite)
- JSONB columns allow schema evolution without migrations

---

**Data Model Status**: ✅ **COMPLETE** - All 7 entities defined with PostgreSQL schema, SQLAlchemy models, indexes, and Alembic migration strategy.
