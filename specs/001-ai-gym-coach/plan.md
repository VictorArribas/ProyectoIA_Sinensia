# Implementation Plan: Smart AI Gym Coach (SAIGC)

**Branch**: `001-ai-gym-coach` | **Date**: 2026-02-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-ai-gym-coach/spec.md`

## Summary

**Smart AI Gym Coach (SAIGC)** is an LLM-powered sports coaching web application that generates personalized workout plans, manages fatigue through adaptive training adjustments, provides nutrition guidance, and offers technical consultation chat. The system prioritizes user safety with evidence-based recommendations, medical disclaimers, and automatic volume reduction when high fatigue or pain is detected.

**Technical Approach**:
- **Backend**: Python 3.11+ with FastAPI for async REST API, SQLAlchemy ORM for PostgreSQL data persistence, Anthropic Claude API for LLM-powered workout generation and chat
- **Frontend**: React 18+ with Vite for SPA development, React Router for navigation, Context API for state management
- **Intelligence**: ML-based fatigue scoring with rule-based fallback, Pydantic-validated LLM responses, progressive overload algorithms based on RPE history
- **Security**: JWT-based authentication, bcrypt password hashing, GDPR-compliant data handling with encryption at rest

**Key Innovation**: Dynamic workout adaptation driven by real-time fatigue analysis (ML model + historical RPE) integrated into LLM prompt context, ensuring safety-first training recommendations.

---

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/TypeScript (frontend - React 18+)
**Primary Dependencies**:
- Backend: FastAPI 0.104+, SQLAlchemy 2.0+ (async), Pydantic v2, Anthropic Python SDK, asyncpg, Alembic
- Frontend: React 18+, Vite 5+, React Router v6, Axios/fetch

**Storage**: PostgreSQL 15+ with JSONB support, ACID compliance for health data integrity
**Testing**: pytest (backend unit/integration), React Testing Library + Vitest (frontend)
**Target Platform**: Web application (SPA) - Linux/Docker backend server, modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
**Project Type**: Web application (backend + frontend monorepo or separate repos)
**Performance Goals**:
- LLM workout generation: <5 seconds per request (p95)
- Macro recalculation: <2 seconds (per SC-004)
- Chat response: <10 seconds (per SC-005)
- API response (non-LLM): <200ms (p95)

**Constraints**:
- Anthropic Claude API rate limits: 4000 req/min (tier 2+ accounts)
- JWT token expiry: 24h (access), 30d (refresh)
- User must explicitly consent to data storage (GDPR)
- Medical disclaimers mandatory on all workout/nutrition outputs

**Scale/Scope**:
- MVP target: 100-500 concurrent users
- Database: ~10k user profiles, ~100k workout logs expected in first 6 months
- LLM token usage: ~500-1500 tokens per workout generation, ~15k tokens/day estimated for MVP

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

### Development Process Gates

✅ **Gate 1: Specification exists**
Status: **PASS** - Complete spec.md with 4 user stories (P1-P4), 27 functional requirements, Technical Deep Dive section

✅ **Gate 2: Simplicity justified**
Status: **PASS** - Web app structure justified: requires backend API (FastAPI) for LLM integration and database persistence, frontend SPA (React) for complex forms and state management (workout logging, profile updates). Simpler alternatives (single HTML file) cannot support authentication, database, or LLM API calls. See Complexity Tracking below.

✅ **Gate 3: User stories independent**
Status: **PASS** - Each user story (P1: Workout Plans, P2: Fatigue Management, P3: Nutrition, P4: Chat) can be tested and deployed independently. P1 is MVP; P2-P4 additive.

✅ **Gate 4: Preview performed**
Status: **N/A** - No visual changes yet (plan phase). Will be enforced during implementation (/implement).

### AI Coaching Compliance Gates

✅ **Gate 5: Safety validation**
Status: **PASS** - FR-008 mandates medical disclaimers. FR-014 denies high-intensity generation for chronic fatigue/pain. Pydantic schema enforces `notas_seguridad` field. Fatigue score >80 triggers volume reduction and medical consultation warning (FR-017b).

✅ **Gate 6: Scientific accuracy**
Status: **PASS** - FR-009 bases recommendations on NSCA/ACSM principles. FR-006 enforces evidence-based volume (10-25 sets/muscle/week). FR-009a implements progressive overload formula with RPE history. Technical Deep Dive references Schoenfeld, Kraemer, Rhea research.

✅ **Gate 7: Privacy by design**
Status: **PASS** - FR-004 treats user data as sensitive health information. PostgreSQL with encryption at rest (assumption #6 updated). FR-000h implements GDPR Right to Erasure. User entity includes email (no PII beyond necessary). JWT tokens stateless (no server-side session storage). Daily backups with 30d retention.

✅ **Gate 8: Clarity check**
Status: **PASS** - FR-023 enforces max 20 words/sentence for instructions. Pydantic validator ensures `notas_seguridad` includes keywords ("espalda", "dolor", "detente"). FR-027 requires beginner-friendly chat responses (8th-grade readability per SC-005).

✅ **Gate 9: Modularity verified**
Status: **PASS** - Backend architecture separates concerns: `models/` (SQLAlchemy entities), `services/` (business logic: fatigue calculation, LLM prompts), `api/` (FastAPI routes). Frontend separates `components/`, `pages/`, `services/` (API client). LLM prompt builder (`build_llm_prompt`) is framework-agnostic pure Python function.

**Constitution Compliance: 9/9 PASS** ✅

---

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-gym-coach/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (tech stack decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (dev setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── auth.yaml        # Authentication endpoints (OpenAPI 3.0)
│   ├── workouts.yaml    # Workout plan generation endpoints
│   ├── fatigue.yaml     # Fatigue logging and scoring endpoints
│   ├── nutrition.yaml   # Nutrition calculation endpoints
│   └── chat.yaml        # Technical consultation chat endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks - NOT created yet)
```

### Source Code (repository root)

**Selected Structure**: Web application (backend + frontend)

```text
backend/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   └── env.py                  # Alembic config
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment variables, settings
│   ├── database.py             # SQLAlchemy engine, session factory
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py             # User, UserProfile entities
│   │   ├── workout.py          # WorkoutPlan, WorkoutLog entities
│   │   ├── exercise.py         # Exercise entity (seed data)
│   │   ├── nutrition.py        # NutritionPlan entity
│   │   └── chat.py             # ChatSession entity
│   ├── schemas/                # Pydantic models (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py             # Login, Register, Token schemas
│   │   ├── workout.py          # ExerciseBlock, WorkoutPlan schemas
│   │   ├── fatigue.py          # WorkoutLogInput, FatigueScore schemas
│   │   ├── nutrition.py        # NutritionPlan schema
│   │   └── chat.py             # ChatRequest, ChatResponse schemas
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py     # JWT generation, password hashing
│   │   ├── fatigue_service.py  # Fatigue score calculation (ML + fallback)
│   │   ├── llm_service.py      # Anthropic Claude API client, prompt builder
│   │   ├── workout_service.py  # Workout generation orchestration
│   │   ├── nutrition_service.py # TDEE, macro calculations
│   │   └── exercise_service.py  # Exercise library queries
│   ├── api/                    # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── auth.py             # POST /register, /login, /refresh
│   │   ├── profile.py          # GET/PUT /profile
│   │   ├── workouts.py         # POST /workouts/generate, GET /workouts/history
│   │   ├── fatigue.py          # POST /workouts/log, GET /fatigue/score
│   │   ├── nutrition.py        # GET /nutrition/calculate
│   │   └── chat.py             # POST /chat/ask
│   ├── middleware/             # Auth middleware, CORS, rate limiting
│   │   ├── __init__.py
│   │   ├── auth_middleware.py  # JWT validation
│   │   └── rate_limit.py       # Rate limiting for auth endpoints
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── validators.py       # Custom Pydantic validators
│       └── exceptions.py       # Custom exception classes
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures (test DB, mock LLM)
│   ├── unit/                   # Unit tests (services, utils)
│   │   ├── test_fatigue_service.py
│   │   ├── test_llm_service.py
│   │   └── test_nutrition_service.py
│   ├── integration/            # Integration tests (API endpoints)
│   │   ├── test_auth_flow.py
│   │   ├── test_workout_generation.py
│   │   └── test_fatigue_adaptation.py
│   └── contract/               # Contract tests (Pydantic schema validation)
│       └── test_llm_schemas.py
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── Dockerfile                  # Docker image for backend
└── README.md                   # Backend setup instructions

frontend/
├── public/                     # Static assets
│   └── index.html
├── src/
│   ├── main.jsx                # React app entry point
│   ├── App.jsx                 # Root component with routing
│   ├── components/             # Reusable UI components
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── workout/
│   │   │   ├── WorkoutTable.jsx          # Display workout plan
│   │   │   ├── WorkoutLogForm.jsx        # Log RPE and pain
│   │   │   └── ExerciseCard.jsx          # Individual exercise display
│   │   ├── nutrition/
│   │   │   └── MacroDisplay.jsx          # Show TDEE and macros
│   │   ├── chat/
│   │   │   └── ChatInterface.jsx         # Chat UI for consultation
│   │   └── common/
│   │       ├── Header.jsx
│   │       ├── Spinner.jsx               # Loading indicator
│   │       └── ErrorBoundary.jsx
│   ├── pages/                  # Page-level components (routes)
│   │   ├── HomePage.jsx        # Landing page
│   │   ├── LoginPage.jsx       # Login/register
│   │   ├── ProfilePage.jsx     # User profile + onboarding
│   │   ├── WorkoutPage.jsx     # Workout plan generation + logging
│   │   ├── NutritionPage.jsx   # Nutrition calculator
│   │   └── ChatPage.jsx        # Technical consultation
│   ├── services/               # API client (Axios)
│   │   ├── api.js              # Axios instance with JWT interceptor
│   │   ├── authService.js      # login(), register(), refreshToken()
│   │   ├── workoutService.js   # generateWorkout(), logWorkout()
│   │   ├── nutritionService.js # getNutrition()
│   │   └── chatService.js      # sendMessage()
│   ├── context/                # React Context for global state
│   │   ├── AuthContext.jsx     # User auth state, token management
│   │   └── ProfileContext.jsx  # User profile data
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.js          # Access auth context
│   │   └── useApi.js           # Generic API call hook with loading/error
│   ├── utils/                  # Utilities
│   │   └── validators.js       # Frontend input validation
│   └── styles/                 # CSS/Tailwind
│       └── index.css           # Global styles
├── tests/                      # Frontend tests (Vitest + RTL)
│   ├── components/
│   │   └── WorkoutTable.test.jsx
│   └── services/
│       └── authService.test.js
├── package.json                # Node dependencies
├── vite.config.js              # Vite configuration
├── .env.example                # Frontend env vars (API base URL)
└── README.md                   # Frontend setup instructions

.specify/                       # Speckit configuration (already exists)
.claude/                        # Claude Code configuration (already exists)
.gitignore                      # Git ignore (node_modules, __pycache__, .env)
README.md                       # Project root README (links to backend/frontend)
docker-compose.yml              # Docker Compose for local dev (PostgreSQL, backend, frontend)
```

**Structure Decision**:
Selected **Web application (backend + frontend)** structure because:
1. **Backend API required**: LLM integration (Anthropic Claude), database persistence (PostgreSQL), business logic (fatigue scoring, progressive overload)
2. **Frontend SPA required**: Complex forms (profile onboarding, workout logging), real-time state (auth, workout plans), multi-page navigation
3. **Separation of concerns**: Backend focuses on data + AI logic, frontend focuses on UX/presentation
4. **Scalability**: Independent deployment/scaling of backend API (compute-heavy LLM calls) vs frontend (static files served via CDN)
5. **Team structure**: Enables parallel development (backend vs frontend teams)

Alternative rejected: Single HTML file (Constitution Principle III) - insufficient for auth, database, LLM API integration, and complex state management.

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **Web app structure (backend + frontend)** | Requires database (PostgreSQL) for multi-user persistence, LLM API calls (Anthropic), JWT auth, complex business logic (fatigue scoring, progressive overload formulas) | Single HTML file with inline CSS cannot: (1) call LLM APIs server-side (exposes API keys), (2) persist data across sessions, (3) handle authentication securely, (4) run ML fatigue model |
| **React framework** | Complex state management (auth tokens, user profile, workout logs, fatigue scores) and forms (multi-step onboarding, RPE logging with conditionals) | Vanilla JS would require manual state sync, form validation, and routing - estimated 3x more code. React Context + hooks reduce boilerplate. |
| **SQLAlchemy ORM** | Type-safe database access, automatic migrations (Alembic), relationship management (User -> WorkoutLog FK), async support for non-blocking queries | Raw SQL queries risk injection attacks, require manual schema versioning, no type hints. Direct `asyncpg` lacks relationship management for 6+ related entities. |
| **Anthropic Claude API (paid)** | Constitutional AI reduces hallucination risk (critical for medical safety), structured outputs via tool use (Pydantic validation), better safety alignment for health domain | Open-source local LLMs (Llama 3, Mistral) lack Constitutional AI training, require GPU server ($200+/month), higher hallucination risk for safety-critical coaching. Cost justified: ~$50-150/month for 100-500 users at MVP scale. |

**Justification Summary**: Complexity necessary for multi-user web app with AI integration, database persistence, and safety-critical health data handling. Simpler alternatives (static HTML, vanilla JS, raw SQL, local LLMs) fail to meet functional requirements (auth, persistence, safety) or increase development risk.

---

## Phase 0: Research Summary

See [research.md](./research.md) for full details. Key decisions:

### 1. LLM Provider: Anthropic Claude
**Decision**: Use Anthropic Claude 3.5 Sonnet via API
**Rationale**:
- Constitutional AI training prioritizes safety (critical for medical disclaimers, pain detection)
- Native structured outputs via tool use (Pydantic schemas without prompt engineering)
- Lower hallucination rates vs GPT-4 in safety-critical domains
- Pricing competitive: $3/1M input tokens, $15/1M output tokens (~$0.03-0.05 per workout generation)

**Alternatives considered**: OpenAI GPT-4 (higher cost, less safety-focused), Local LLMs (requires GPU, no Constitutional AI)

### 2. Backend Framework: Python + FastAPI
**Decision**: Python 3.11+ with FastAPI 0.104+
**Rationale**:
- Native Pydantic v2 integration (schemas already defined in spec)
- Async support for non-blocking LLM calls (asyncio + asyncpg)
- ML ecosystem compatibility (scikit-learn, TensorFlow for future fatigue model)
- Auto-generated OpenAPI docs (Swagger UI for frontend integration)

**Alternatives considered**: Node.js + Express (less ML ecosystem), Django (overkill, no native async), Go (limited ML libs)

### 3. Authentication: Email/Password + JWT
**Decision**: JWT tokens (HS256) with bcrypt password hashing
**Rationale**:
- Stateless tokens (no Redis/session storage required at MVP scale)
- GDPR-compliant (users own their accounts, can delete data via FR-000h)
- Simple password reset flow (email token -> reset endpoint)
- Rate limiting on auth endpoints (5 attempts / 15 min per FR-000g)

**Alternatives considered**: OAuth only (adds third-party dependency), No auth (violates data privacy principle)

### 4. Frontend: React + Vite
**Decision**: React 18+ with Vite 5+ build tool
**Rationale**:
- Component reusability (forms, workout tables)
- Context API sufficient for MVP state (no Redux complexity)
- Vite HMR faster than Webpack (dev experience)
- TypeScript optional but recommended (type-safe API contracts)

**Alternatives considered**: Vue 3 (smaller community), Svelte (less mature ecosystem), Vanilla JS (3x more boilerplate)

### 5. Database: PostgreSQL
**Decision**: PostgreSQL 15+ with SQLAlchemy 2.0+ async ORM
**Rationale**:
- ACID compliance (critical for health data integrity)
- JSONB columns for flexible workout plan storage
- Proven at scale (millions of rows)
- Alembic migrations for schema versioning

**Alternatives considered**: SQLite (no concurrency), MongoDB (no ACID multi-doc), MySQL (less advanced JSON support)

### 6. Deployment Strategy (Future)
**Deferred to implementation**: Docker Compose for local dev, consider Render/Railway/Fly.io for MVP hosting. Backend needs: 2 vCPU, 4GB RAM, PostgreSQL instance. Frontend: Static hosting (Vercel/Netlify).

---

## Phase 1: Design Artifacts

### Data Model
See [data-model.md](./data-model.md) for complete SQLAlchemy models. Key entities:

**Core Tables**:
1. `users` - Authentication (email, hashed_password, created_at, email_verified)
2. `user_profiles` - Fitness data (age, weight, objective, experience_level, equipment, injury_history)
3. `exercises` - Exercise library (name, muscle_groups, equipment_required, difficulty, safety_notes, contraindications)
4. `workout_plans` - Generated plans (user_id, plan_data JSONB, fatigue_score_used, created_at)
5. `workout_logs` - Post-workout RPE/pain (user_id, workout_plan_id, rpe, pain_reported, pain_location, logged_at)
6. `nutrition_plans` - Macro recommendations (user_id, tdee, protein_g, carbs_g, fats_g, calories, updated_at)
7. `chat_sessions` - Consultation history (user_id, question, response, category, created_at)

**Relationships**:
- User 1:1 UserProfile
- User 1:N WorkoutPlan, WorkoutLog, NutritionPlan, ChatSession
- WorkoutPlan 1:N WorkoutLog

### API Contracts
See [contracts/](./contracts/) for OpenAPI 3.0 specs. Key endpoints:

**Authentication** (`contracts/auth.yaml`):
- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Get JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Invalidate refresh token

**Workout Management** (`contracts/workouts.yaml`):
- `POST /api/v1/workouts/generate` - Generate workout plan (calls LLM)
- `GET /api/v1/workouts/history` - Get past workout plans
- `POST /api/v1/workouts/log` - Log RPE and pain after workout
- `GET /api/v1/workouts/current` - Get active workout plan

**Fatigue Scoring** (`contracts/fatigue.yaml`):
- `GET /api/v1/fatigue/score` - Get current fatigue score (0-100)
- `GET /api/v1/fatigue/history` - Get fatigue trend graph data

**Nutrition** (`contracts/nutrition.yaml`):
- `GET /api/v1/nutrition/calculate` - Calculate TDEE and macros
- `PUT /api/v1/nutrition/update` - Recalculate after weight change

**Chat** (`contracts/chat.yaml`):
- `POST /api/v1/chat/ask` - Send technique/equipment question to LLM
- `GET /api/v1/chat/history` - Get past chat sessions

### Quickstart Guide
See [quickstart.md](./quickstart.md) for developer setup instructions:
1. Prerequisites (Python 3.11+, Node 18+, PostgreSQL 15+, Docker optional)
2. Backend setup (venv, pip install, .env config, DB migrations, seed exercises)
3. Frontend setup (npm install, .env config, dev server)
4. Testing (pytest, Vitest)
5. Docker Compose workflow (full stack in one command)

---

## Phase 1: Constitution Re-Check

**Post-design validation**: All 9 gates still **PASS** ✅

**Changes from Phase 0**:
- Gate 2 updated: Web app structure justified in Complexity Tracking table
- Gate 7 updated: Data model confirms User entity separation, no excessive PII storage
- Gate 9 updated: Source structure confirms modularity (models, services, api layers)

**No violations introduced during design phase.**

---

## Next Steps

1. ✅ **Phase 0 complete**: research.md created with tech stack decisions
2. ✅ **Phase 1 complete**: data-model.md, contracts/, quickstart.md created
3. ⏭️ **Phase 2 pending**: Run `/speckit.tasks` to generate tasks.md from this plan
4. ⏭️ **Implementation**: Run `/speckit.implement` to execute tasks

**Artifacts Created**:
- `specs/001-ai-gym-coach/plan.md` (this file)
- `specs/001-ai-gym-coach/research.md` (Phase 0)
- `specs/001-ai-gym-coach/data-model.md` (Phase 1)
- `specs/001-ai-gym-coach/quickstart.md` (Phase 1)
- `specs/001-ai-gym-coach/contracts/*.yaml` (Phase 1)

**Ready for task generation**: ✅ All design artifacts complete. Spec + Plan + Data Model + Contracts provide sufficient detail for `/speckit.tasks` to generate actionable, dependency-ordered task list.
