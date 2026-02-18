# Tasks: Smart AI Gym Coach (SAIGC)

**Feature**: 001-ai-gym-coach
**Input**: Design documents from `specs/001-ai-gym-coach/` (plan.md, spec.md, data-model.md, contracts/)
**Prerequisites**: Phase 0 (research.md) and Phase 1 (plan.md, data-model.md) design complete

**Tests**: Per spec.md, tests are **OPTIONAL** - only included if explicitly requested. Focus on manual browser testing (Constitution Principle IV).

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each P1-P4 story.

---

## Format: `[TaskID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

**Backend**: `backend/src/`, `backend/tests/`
**Frontend**: `frontend/src/`, `frontend/tests/`
**Database**: `backend/alembic/versions/`
**Shared**: Repository root (`docker-compose.yml`, `README.md`)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create repository structure, initialize backend/frontend projects, configure environment

- [X] T001 Create repository root structure: `backend/`, `frontend/`, `.gitignore`, `README.md`, `docker-compose.yml`
- [X] T002 [P] Initialize Python backend: `cd backend && python3.11 -m venv venv && pip install fastapi sqlalchemy alembic anthropic asyncpg pydantic pytest`
- [X] T003 [P] Create `backend/requirements.txt` with pinned versions (FastAPI 0.104+, SQLAlchemy 2.0+, Pydantic v2, anthropic, asyncpg, alembic, bcrypt, python-jose)
- [X] T004 [P] Initialize React frontend: `cd frontend && npm create vite@latest . -- --template react && npm install react-router-dom axios`
- [X] T005 [P] Create `backend/.env.example` with environment variable template (DATABASE_URL, JWT_SECRET_KEY, ANTHROPIC_API_KEY)
- [X] T006 [P] Create `frontend/.env.example` with `VITE_API_BASE_URL=http://localhost:8000/api/v1`
- [X] T007 Configure Docker Compose with PostgreSQL 15, backend, frontend services in `docker-compose.yml`
- [X] T008 Create backend entry point `backend/src/main.py` with FastAPI app initialization, CORS middleware, router includes
- [X] T009 Create frontend entry point `frontend/src/main.jsx` with React 18 + StrictMode + BrowserRouter
- [X] T010 [P] Configure backend linting: create `backend/.ruff.toml` and `backend/pyproject.toml` for black formatter

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [X] T011 Create SQLAlchemy engine configuration in `backend/src/database.py` with async session factory (asyncpg driver)
- [X] T012 Initialize Alembic in `backend/`: run `alembic init alembic` and configure `alembic.ini` with DATABASE_URL
- [X] T013 Create PostgreSQL ENUM types in `backend/alembic/env.py`: `fitness_objective`, `experience_level`
- [ ] T014 Create initial migration `backend/alembic/versions/001_initial_schema.py` with all 7 tables (users, user_profiles, exercises, workout_plans, workout_logs, nutrition_plans, chat_sessions)
- [ ] T015 Run migration: `cd backend && alembic upgrade head` to create tables

### Authentication & User Management

- [X] T016 Create User SQLAlchemy model in `backend/src/models/user.py` with email, password_hash, created_at, relationships
- [X] T017 Create UserProfile SQLAlchemy model in `backend/src/models/user_profile.py` with biometric data, fitness params, FK to User
- [X] T018 Create Pydantic schemas for auth in `backend/src/schemas/auth.py`: RegisterRequest, LoginRequest, TokenResponse
- [X] T019 Implement password hashing utilities in `backend/src/services/auth_service.py`: `hash_password()`, `verify_password()` using bcrypt
- [X] T020 Implement JWT token generation in `backend/src/services/auth_service.py`: `create_access_token()`, `create_refresh_token()` using python-jose
- [X] T021 Create JWT auth middleware in `backend/src/middleware/auth_middleware.py`: `get_current_user()` dependency for protected routes
- [X] T022 Create auth API routes in `backend/src/api/auth.py`: POST /register, POST /login, POST /refresh
- [X] T023 Create rate limiting middleware in `backend/src/middleware/rate_limit.py`: 5 attempts/15min for login endpoint (FR-000g)

### Exercise Library (Seed Data)

- [X] T024 Create Exercise SQLAlchemy model in `backend/src/models/exercise.py` with name, muscle_groups, safety_notes, volume_guidelines_json
- [X] T025 Create exercise seed script `backend/scripts/seed_exercises.py` with 50-100 exercises (Spanish names, technique cues, contraindications)
- [ ] T026 Run seed script: `cd backend && python scripts/seed_exercises.py` to populate exercises table

### Frontend Auth Context

- [X] T027 Create Axios API client in `frontend/src/services/api.js` with baseURL, JWT interceptor for Authorization header
- [X] T028 Create AuthContext in `frontend/src/context/AuthContext.jsx` with login(), logout(), register(), token state, user email
- [X] T029 Create auth service in `frontend/src/services/authService.js` with API calls to /auth/register, /auth/login, /auth/refresh

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Profile & Workout Plan Generation (Priority: P1) 🎯 MVP

**Goal**: Users can create profile, receive personalized workout plan with evidence-based volume, see medical disclaimer

**Independent Test**: Register → create profile (age, weight, objective, equipment) → generate workout plan → see table with exercises/sets/reps/RPE → verify medical disclaimer present

### Backend Implementation (US1)

- [X] T030 [P] [US1] Create UserProfile Pydantic schemas in `backend/src/schemas/profile.py`: UserProfileCreate, UserProfileUpdate, UserProfileResponse
- [X] T031 [P] [US1] Create WorkoutPlan model in `backend/src/models/workout_plan.py` with plan_data JSONB, fatigue_score_used, FK to User
- [X] T032 [P] [US1] Create WorkoutPlan Pydantic schema in `backend/src/schemas/workout.py`: ExerciseBlock, WorkoutPlan (from spec.md Technical Deep Dive)
- [X] T033 [US1] Implement LLM service in `backend/src/services/llm_service.py`: `build_llm_prompt()` function with fatigue score injection (from spec.md)
- [X] T034 [US1] Implement LLM service `call_anthropic_claude()` in `backend/src/services/llm_service.py` using anthropic SDK with WorkoutPlan tool use
- [X] T035 [US1] Implement workout service in `backend/src/services/workout_service.py`: `generate_workout_plan()` orchestrates exercise selection, LLM call, Pydantic validation
- [X] T036 [US1] Implement profile service in `backend/src/services/profile_service.py`: get_user_profile(), create_user_profile(), update_user_profile()
- [X] T037 [US1] Create profile API routes in `backend/src/api/profile.py`: POST /profile/create, GET /profile/me, PUT /profile/update
- [X] T038 [US1] Create workout API routes in `backend/src/api/workouts.py`: POST /workouts/generate (calls LLM, inserts workout_plan), GET /workouts/history

### Frontend Implementation (US1)

- [X] T039 [P] [US1] Create ProfileForm component in `frontend/src/components/ProfileForm.jsx` with onboarding form fields
- [X] T040 [P] [US1] Create profile service in `frontend/src/services/profileService.js` with API calls to /profile endpoints
- [X] T041 [P] [US1] Create workout service in `frontend/src/services/workoutService.js` with API call to POST /workouts/generate
- [X] T042 [US1] Create ProfilePage component in `frontend/src/pages/ProfilePage.jsx` with onboarding form (age, weight, objective, experience_level, training_days_per_week, equipment checkboxes, injuries text area)
- [X] T043 [US1] Create WorkoutsPage component in `frontend/src/pages/WorkoutsPage.jsx` with "Generate Workout Plan" button
- [X] T044 [US1] Create WorkoutTable component in `frontend/src/components/WorkoutTable.jsx` to display ExerciseBlock[] in table format (columns: Ejercicio, Músculo, Series, Repeticiones, RPE Objetivo, Descanso, Notas de Seguridad)
- [X] T045 [US1] Add medical disclaimer display to WorkoutTable component (from plan_data.disclaimer_medico)
- [X] T046 [US1] Create routing in `frontend/src/App.jsx`: /login, /register, /profile, /workouts with Navbar

### Validation & Integration (US1)

- [ ] T047 [US1] Validate FR-006: Verify generated workout plans respect volume guidelines (10-15 sets/muscle for beginners, 15-20 for intermediate, 20-25 for advanced)
- [ ] T048 [US1] Validate FR-007a: Confirm all ExerciseBlock fields present (musculo, ejercicio, series, repeticiones, rpe_objetivo, descanso_segundos, notas_seguridad)
- [ ] T049 [US1] Validate FR-008: Confirm medical disclaimer appears on every workout plan in UI
- [ ] T050 [US1] Manual browser test: Complete full user journey from registration → profile creation → workout generation → view plan in table

**Checkpoint**: User Story 1 (MVP) fully functional and testable independently. Deploy/demo ready.

---

## Phase 4: User Story 2 - Fatigue Management & Adaptive Training (Priority: P2)

**Goal**: Users log RPE and pain after workouts, system auto-adjusts next workout volume based on fatigue score

**Independent Test**: Complete US1 → log workout with high RPE (9) or pain → generate next workout → verify volume reduced 20-30% and warning message displayed

### Backend Implementation (US2)

- [ ] T051 [P] [US2] Create WorkoutLog model in `backend/src/models/workout_log.py` with rpe, pain_reported, pain_location, FK to User and WorkoutPlan
- [ ] T052 [P] [US2] Create WorkoutLog Pydantic schemas in `backend/src/schemas/fatigue.py`: WorkoutLogCreate, WorkoutLogResponse, FatigueScoreResponse
- [ ] T053 [US2] Implement rule-based fatigue calculation in `backend/src/services/fatigue_service.py`: `calculate_fatigue_score_fallback()` (from spec.md Technical Deep Dive)
- [ ] T054 [US2] Implement fatigue service `get_fatigue_score()` in `backend/src/services/fatigue_service.py` with ML model attempt + fallback (from spec.md line 526-545)
- [ ] T055 [US2] Implement fatigue rules mapper in `backend/src/services/fatigue_service.py`: `map_fatigue_category()` returns adjustment based on score (from FR-017b table)
- [ ] T056 [US2] Update workout service `generate_workout_plan()` in `backend/src/services/workout_service.py` to call `get_fatigue_score()` and apply volume adjustment
- [ ] T057 [US2] Update LLM prompt builder in `backend/src/services/llm_service.py` to inject fatigue score and adjustment rules (from spec.md SYSTEM_PROMPT_TEMPLATE)
- [ ] T058 [US2] Create fatigue API routes in `backend/src/api/fatigue.py`: POST /fatigue/logs (log workout), GET /fatigue/score, GET /fatigue/logs (history)

### Frontend Implementation (US2)

- [ ] T059 [P] [US2] Create fatigue service in `frontend/src/services/fatigueService.js` with API calls to /fatigue/logs and /fatigue/score
- [ ] T060 [US2] Create WorkoutLogForm component in `frontend/src/components/workout/WorkoutLogForm.jsx` with RPE slider (1-10), pain checkbox, pain location input
- [ ] T061 [US2] Add WorkoutLogForm to WorkoutPage after workout table display
- [ ] T062 [US2] Create FatigueDisplay component in `frontend/src/components/workout/FatigueDisplay.jsx` showing current fatigue score (0-100) with color coding (green <40, yellow 40-60, orange 60-80, red >80)
- [ ] T063 [US2] Add fatigue score display to WorkoutPage header
- [ ] T064 [US2] Display volume adjustment message in WorkoutTable when `ajuste_aplicado` is present (e.g., "Volumen reducido 30% por fatiga alta")

### Validation & Integration (US2)

- [ ] T065 [US2] Validate FR-012: Log RPE 9-10 or pain → verify next workout volume reduced 20-30%
- [ ] T066 [US2] Validate FR-013: Log 3 consecutive sessions with RPE 8+ → verify deload week (50% reduction) suggested
- [ ] T067 [US2] Validate FR-015: Log 2 weeks of RPE 3-5 → verify next workout volume increased 5-10%
- [ ] T068 [US2] Validate FR-016: Log pain in "shoulder" → verify next workout excludes overhead press and lateral raises
- [ ] T069 [US2] Manual browser test: Complete workout logging flow with high fatigue → verify adaptation in next plan

**Checkpoint**: User Stories 1 AND 2 both work independently. Fatigue-driven adaptation functional.

---

## Phase 5: User Story 3 - Nutrition Calculator (Priority: P3)

**Goal**: Users input profile data, receive TDEE and macro targets, macros auto-recalculate when weight changes

**Independent Test**: Access nutrition page → see calculated TDEE, protein/carbs/fat targets → update weight in profile → return to nutrition page → verify macros recalculated

### Backend Implementation (US3)

- [ ] T070 [P] [US3] Create NutritionPlan model in `backend/src/models/nutrition_plan.py` with tdee, protein_g, carbs_g, fat_g, FK to User
- [ ] T071 [P] [US3] Create NutritionPlan Pydantic schema in `backend/src/schemas/nutrition.py`: NutritionPlanResponse with tdee, target_calories, macros, disclaimer
- [ ] T072 [US3] Implement TDEE calculation in `backend/src/services/nutrition_service.py`: `calculate_tdee()` using Mifflin-St Jeor equation (from spec.md assumption #4)
- [ ] T073 [US3] Implement macro calculation in `backend/src/services/nutrition_service.py`: `calculate_macros()` based on objective (from FR-019 rules)
- [ ] T074 [US3] Implement nutrition service `get_nutrition_plan()` in `backend/src/services/nutrition_service.py` that upserts NutritionPlan on user_id
- [ ] T075 [US3] Create nutrition API routes in `backend/src/api/nutrition.py`: GET /nutrition/calculate (returns NutritionPlan)
- [ ] T076 [US3] Add database trigger or service hook to recalculate nutrition when UserProfile.weight updates (FR-020)

### Frontend Implementation (US3)

- [ ] T077 [P] [US3] Create nutrition service in `frontend/src/services/nutritionService.js` with API call to GET /nutrition/calculate
- [ ] T078 [US3] Create NutritionPage component in `frontend/src/pages/NutritionPage.jsx`
- [ ] T079 [US3] Create MacroDisplay component in `frontend/src/components/nutrition/MacroDisplay.jsx` showing TDEE, target calories, protein/carbs/fat in grams and percentages
- [ ] T080 [US3] Add nutrition disclaimer to MacroDisplay (from FR-021)
- [ ] T081 [US3] Add /nutrition route to `frontend/src/App.jsx`
- [ ] T082 [US3] Add "Recalculate" button to NutritionPage that fetches updated plan after weight change

### Validation & Integration (US3)

- [ ] T083 [US3] Validate FR-019: Hypertrophy objective → verify protein 1.6-2.2g/kg, calories TDEE+10-20%
- [ ] T084 [US3] Validate FR-019: Definition objective → verify protein 2.0-2.4g/kg, calories TDEE-15-25%
- [ ] T085 [US3] Validate FR-020: Update user weight → return to nutrition page → verify macros recalculated
- [ ] T086 [US3] Validate SC-004: Macro recalculation completes within 2 seconds
- [ ] T087 [US3] Manual browser test: Complete nutrition flow → update weight → verify auto-recalculation

**Checkpoint**: User Stories 1, 2, AND 3 all work independently. Nutrition calculation functional.

---

## Phase 6: User Story 4 - Technical Consultation Chat (Priority: P4)

**Goal**: Users ask technique/equipment/concept questions, receive evidence-based beginner-friendly answers, system refuses medical diagnosis

**Independent Test**: Access chat page → ask "How do I do a proper squat?" → receive step-by-step instructions → ask "Why does my knee hurt?" → receive medical refusal

### Backend Implementation (US4)

- [ ] T088 [P] [US4] Create ChatSession model in `backend/src/models/chat_session.py` with question, response, question_category, FK to User
- [ ] T089 [P] [US4] Create ChatSession Pydantic schemas in `backend/src/schemas/chat.py`: ChatRequest, ChatResponse
- [ ] T090 [US4] Implement question classifier in `backend/src/services/llm_service.py`: `classify_question_category()` detects medical-diagnosis questions (FR-025)
- [ ] T091 [US4] Implement chat service in `backend/src/services/chat_service.py`: `generate_chat_response()` calls Anthropic Claude with beginner-friendly system prompt
- [ ] T092 [US4] Implement medical refusal template in `backend/src/services/chat_service.py`: returns standard message for medical-diagnosis category (from spec.md line 506)
- [ ] T093 [US4] Create chat API routes in `backend/src/api/chat.py`: POST /chat/ask (question → response), GET /chat/history

### Frontend Implementation (US4)

- [ ] T094 [P] [US4] Create chat service in `frontend/src/services/chatService.js` with API calls to POST /chat/ask and GET /chat/history
- [ ] T095 [US4] Create ChatPage component in `frontend/src/pages/ChatPage.jsx`
- [ ] T096 [US4] Create ChatInterface component in `frontend/src/components/chat/ChatInterface.jsx` with message list (user/assistant bubbles) and input form
- [ ] T097 [US4] Add /chat route to `frontend/src/App.jsx`
- [ ] T098 [US4] Style medical refusal messages differently (warning/alert style) in ChatInterface

### Validation & Integration (US4)

- [ ] T099 [US4] Validate FR-023: Ask "How do I perform a proper squat?" → verify response includes step-by-step instructions (max 20 words/sentence)
- [ ] T100 [US4] Validate FR-024: Ask "I don't have a cable machine, what can I do?" → verify response suggests evidence-based alternatives (pull-ups, dumbbell rows)
- [ ] T101 [US4] Validate FR-025: Ask "Why does my knee crack during squats?" → verify system refuses diagnosis and recommends healthcare professional
- [ ] T102 [US4] Validate SC-005: Chat response generated within 10 seconds
- [ ] T103 [US4] Validate FR-027: Verify chat responses are beginner-friendly (readable at 8th-grade level)
- [ ] T104 [US4] Manual browser test: Complete chat flow → test technique, equipment, concept, and medical questions

**Checkpoint**: All 4 user stories (P1-P4) independently functional. MVP complete with all features.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories, documentation, performance optimization

- [ ] T105 [P] Create comprehensive README.md in repository root with project overview, quickstart instructions, link to specs/
- [ ] T106 [P] Create backend README.md in `backend/README.md` with API documentation, environment setup, testing instructions
- [ ] T107 [P] Create frontend README.md in `frontend/README.md` with component structure, routing, state management explanation
- [ ] T108 [P] Add loading spinners to all API calls in frontend (WorkoutPage, NutritionPage, ChatPage) using Spinner component in `frontend/src/components/common/Spinner.jsx`
- [ ] T109 [P] Add error boundary in `frontend/src/components/common/ErrorBoundary.jsx` to catch React errors and display fallback UI
- [ ] T110 [P] Implement pagination for workout history in `backend/src/api/workouts.py` GET /workouts/history endpoint (limit=20, offset query params)
- [ ] T111 [P] Implement pagination for workout logs in `backend/src/api/fatigue.py` GET /fatigue/logs endpoint
- [ ] T112 [P] Add input validation error messages to all forms (ProfilePage, WorkoutLogForm) with clear field-level errors
- [ ] T113 Add responsive design CSS to frontend for mobile devices (media queries in `frontend/src/styles/index.css`)
- [ ] T114 Add dark mode toggle to frontend Header component (optional enhancement)
- [ ] T115 Performance optimization: Add database indexes on frequently queried columns (workout_plans.user_id, workout_logs.logged_at, chat_sessions.user_id)
- [ ] T116 Security audit: Run `safety check` on backend dependencies, update vulnerable packages
- [ ] T117 Run Constitution Principle IV manual QA: Preview `index.html` in browser, verify all pages load correctly, test navigation, verify visual consistency
- [ ] T118 Create deployment documentation in `DEPLOYMENT.md` with Docker deployment instructions, environment variables reference, database backup procedures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) completion - **May integrate with US1** (uses workout_plans) but independently testable
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) completion - No dependencies on other stories (only uses UserProfile)
- **User Story 4 (Phase 6)**: Depends on Foundational (Phase 2) completion - No dependencies on other stories
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Independence

✅ **User Story 1 (P1)**: Fully independent - can deploy as standalone MVP
✅ **User Story 2 (P2)**: Reads workout_plans created by US1 but can be tested independently by manually creating test data
✅ **User Story 3 (P3)**: Fully independent - only reads UserProfile
✅ **User Story 4 (P4)**: Fully independent - stateless chat with LLM

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T002 (backend init) || T004 (frontend init)
- T003 (requirements.txt) || T006 (frontend .env.example) || T010 (linting config)

**Within Foundational (Phase 2)**:
- T016 (User model) || T017 (UserProfile model) || T024 (Exercise model)
- T018 (auth schemas) || T030 (profile schemas) || T032 (workout schemas)
- T027 (Axios client) || T028 (AuthContext) || T029 (auth service)

**Within User Story 1 (Phase 3)**:
- T030 (profile schemas) || T031 (WorkoutPlan model) || T032 (workout schemas)
- T039 (ProfileContext) || T040 (profile service) || T041 (workout service)

**Within User Story 2 (Phase 4)**:
- T051 (WorkoutLog model) || T052 (fatigue schemas)
- T059 (fatigue service) || T062 (FatigueDisplay component)

**Within User Story 3 (Phase 5)**:
- T070 (NutritionPlan model) || T071 (nutrition schemas)
- T077 (nutrition service) || T079 (MacroDisplay component)

**Within User Story 4 (Phase 6)**:
- T088 (ChatSession model) || T089 (chat schemas)
- T094 (chat service) || T096 (ChatInterface component)

**Within Polish (Phase 7)**:
- T105 (root README) || T106 (backend README) || T107 (frontend README)
- T108 (spinners) || T109 (error boundary) || T112 (validation errors)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (**10 tasks**)
2. Complete Phase 2: Foundational (**16 tasks**, CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (**21 tasks**)
4. **STOP and VALIDATE**: Test User Story 1 independently (T050 manual browser test)
5. Deploy/demo MVP (workout plan generation)

**Total MVP tasks**: **47 tasks**

### Incremental Delivery (Recommended)

1. **Week 1-2**: Setup + Foundational → Foundation ready (26 tasks)
2. **Week 3**: User Story 1 → Test independently → Deploy MVP (21 tasks) ✅ **MVP DEPLOYED**
3. **Week 4**: User Story 2 → Test independently → Deploy fatigue adaptation (19 tasks) ✅ **Adaptive Training LIVE**
4. **Week 5**: User Story 3 → Test independently → Deploy nutrition calculator (18 tasks) ✅ **Nutrition LIVE**
5. **Week 6**: User Story 4 → Test independently → Deploy chat consultation (17 tasks) ✅ **Full Feature Set LIVE**
6. **Week 7**: Polish & Cross-Cutting → Documentation, optimization (14 tasks) ✅ **Production Ready**

**Total tasks**: **115 tasks** (7 weeks at ~16 tasks/week)

### Parallel Team Strategy

With 3 developers after Foundational phase complete:

**Week 3-4**:
- Developer A: User Story 1 (21 tasks)
- Developer B: User Story 2 (19 tasks)
- Developer C: User Story 3 (18 tasks)

**Week 5-6**:
- Developer A: User Story 4 (17 tasks)
- Developers B+C: Polish & Cross-Cutting (14 tasks shared)

**Team velocity**: ~2-3 weeks for full implementation (vs 7 weeks sequential)

---

## Task Count Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| **Phase 1: Setup** | 10 | Project initialization, backend/frontend setup |
| **Phase 2: Foundational** | 16 | Auth, database, exercise library (BLOCKS all stories) |
| **Phase 3: User Story 1 (P1)** | 21 | User profile + workout plan generation (MVP) |
| **Phase 4: User Story 2 (P2)** | 19 | Fatigue management + adaptive training |
| **Phase 5: User Story 3 (P3)** | 18 | Nutrition calculator (TDEE + macros) |
| **Phase 6: User Story 4 (P4)** | 17 | Technical consultation chat |
| **Phase 7: Polish** | 14 | Documentation, optimization, security audit |
| **TOTAL** | **115 tasks** | Full feature implementation |

---

## Independent Test Criteria Per Story

### User Story 1 (MVP) - Independent Test
**Task T050**: Register account → complete profile (age, weight, objective "hypertrophy", experience "intermediate", equipment "barbell, dumbbells") → click "Generate Workout Plan" → verify table displays exercises with sets/reps/RPE → verify medical disclaimer present → verify 15-20 sets per muscle group (intermediate volume)

### User Story 2 - Independent Test
**Task T069**: Complete US1 workout generation → log workout with RPE 9 and pain_reported=true, pain_location="shoulder" → generate next workout → verify volume reduced by 20-30% → verify warning message "Your recent session indicated high fatigue..." → verify no overhead press in next plan

### User Story 3 - Independent Test
**Task T087**: Navigate to /nutrition → verify TDEE calculated → verify protein target 1.6-2.2g/kg (for hypertrophy) → verify caloric surplus 10-20% → update weight in /profile from 75kg to 80kg → return to /nutrition → verify macros recalculated with new weight → verify disclaimer present

### User Story 4 - Independent Test
**Task T104**: Navigate to /chat → ask "How do I perform a proper squat?" → verify response includes step-by-step instructions (max 20 words/sentence) → ask "Why does my knee hurt during squats?" → verify system refuses with "No puedo proporcionar diagnósticos médicos. Consulta con un profesional de la salud..."

---

## Notes

- **[P] tasks** = different files, no dependencies, can run concurrently
- **[Story] label** = maps task to specific user story for traceability (US1, US2, US3, US4)
- **Constitution Principle IV**: Manual browser testing is standard (T050, T069, T087, T104, T117). Automated tests optional unless explicitly requested.
- **All tasks follow checklist format**: `- [ ] TaskID [P?] [Story?] Description with exact file path`
- Commit after each logical group of tasks (e.g., after completing a service layer, after completing a model)
- Stop at any checkpoint (end of user story phase) to validate story independently before proceeding
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence

---

**Tasks.md Status**: ✅ **COMPLETE** - 115 tasks generated, organized by user story, dependency-ordered, independently testable, ready for `/speckit.implement`.

**Suggested MVP Scope**: **Phase 1 + Phase 2 + Phase 3 (User Story 1)** = 47 tasks for minimal viable product (workout plan generation).

**Recommended Next Command**: `/speckit.implement` to execute tasks from tasks.md
