# Quickstart Guide: Smart AI Gym Coach (SAIGC)

**Feature**: 001-ai-gym-coach
**Date**: 2026-02-18
**For**: Developers setting up local environment

## Prerequisites

- **Python**: 3.11+ (`python --version`)
- **Node.js**: 18+ (`node --version`)
- **PostgreSQL**: 15+ (`psql --version`)
- **Docker**: Optional but recommended (`docker --version`)
- **Git**: For cloning the repository

---

## Option 1: Docker Compose (Recommended)

### 1. Clone Repository & Navigate

```bash
git clone https://github.com/your-org/smart-ai-gym-coach.git
cd smart-ai-gym-coach
```

### 2. Configure Environment Variables

```bash
# Copy example env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**backend/.env**:
```env
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/gym_coach_db

# Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-api-key-here

# Environment
ENVIRONMENT=development
DEBUG=True
```

**frontend/.env**:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Start Services

```bash
docker-compose up -d
```

This starts:
- **PostgreSQL** (port 5432)
- **Backend (FastAPI)** (port 8000)
- **Frontend (React + Vite)** (port 5173)

### 4. Run Migrations & Seed Data

```bash
# Apply database migrations
docker-compose exec backend alembic upgrade head

# Seed exercise library (50-100 exercises)
docker-compose exec backend python scripts/seed_exercises.py
```

### 5. Access Application

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs (Swagger UI)
- **Backend ReDoc**: http://localhost:8000/redoc

### 6. Test Authentication

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123!"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123!"}'
```

---

## Option 2: Manual Setup (Without Docker)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env (see Option 1 for template)
cp .env.example .env
# Edit .env with your Anthropic API key and PostgreSQL connection

# Run migrations
alembic upgrade head

# Seed exercise library
python scripts/seed_exercises.py

# Start backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. PostgreSQL Setup (if not using Docker)

```bash
# Install PostgreSQL 15+
# macOS: brew install postgresql@15
# Ubuntu: sudo apt install postgresql-15
# Windows: Download installer from postgresql.org

# Create database
psql -U postgres
CREATE DATABASE gym_coach_db;
CREATE USER gym_coach_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gym_coach_db TO gym_coach_user;
\q

# Update backend/.env with connection string:
DATABASE_URL=postgresql://gym_coach_user:your_password@localhost:5432/gym_coach_db
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure .env (see Option 1 for template)
cp .env.example .env

# Start dev server
npm run dev
```

Frontend runs at http://localhost:5173

---

## Testing

### Backend Tests (pytest)

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_fatigue_service.py

# Run integration tests (requires test database)
pytest tests/integration/
```

### Frontend Tests (Vitest + React Testing Library)

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- WorkoutTable.test.jsx
```

---

## Development Workflow

### 1. Create a New Branch

```bash
git checkout -b feature/001-user-authentication
```

### 2. Make Changes

Edit files in `backend/src/` or `frontend/src/`

### 3. Run Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

### 4. Check Code Quality

```bash
# Backend: black + ruff
cd backend
black src/ tests/
ruff check src/ tests/

# Frontend: ESLint + Prettier
cd frontend
npm run lint
npm run format
```

### 5. Commit & Push

```bash
git add .
git commit -m "Add user authentication endpoints"
git push origin feature/001-user-authentication
```

---

## Database Migrations (Alembic)

### Create a New Migration

```bash
cd backend

# Auto-generate from SQLAlchemy model changes
alembic revision --autogenerate -m "Add fatigue_score column to workout_plans"

# Review generated migration in alembic/versions/
# Edit if necessary (auto-generation is not perfect)

# Apply migration
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123
```

### View Migration History

```bash
alembic history
alembic current
```

---

## Troubleshooting

### Backend won't start

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**: Check PostgreSQL is running (`docker-compose ps` or `pg_ctl status`)

**Error**: `anthropic.APIError: Invalid API key`
**Solution**: Verify `ANTHROPIC_API_KEY` in backend/.env

### Frontend API calls failing

**Error**: `Network Error` or `CORS policy`
**Solution**: Check backend is running at http://localhost:8000 and `VITE_API_BASE_URL` matches

### Database migrations fail

**Error**: `alembic.util.exc.CommandError: Target database is not up to date.`
**Solution**: Run `alembic upgrade head` before `alembic revision --autogenerate`

### Tests failing

**Error**: `ModuleNotFoundError: No module named 'anthropic'`
**Solution**: Activate virtual environment (`source venv/bin/activate`) and run `pip install -r requirements.txt`

---

## API Documentation

After starting the backend, visit:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Try out endpoints with authentication
  - View request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Alternative documentation view
  - Better for reading full API reference

---

## Project Structure Reference

```
backend/
├── alembic/              # Database migrations
├── src/
│   ├── main.py           # FastAPI app entry point
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic (fatigue, LLM, workout)
│   ├── api/              # FastAPI route handlers
│   └── middleware/       # Auth, CORS, rate limiting
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── .env

frontend/
├── src/
│   ├── main.jsx          # React entry point
│   ├── App.jsx           # Root component with routing
│   ├── components/       # Reusable UI components
│   ├── pages/            # Page-level components
│   ├── services/         # API client (Axios)
│   └── context/          # React Context (auth, profile)
├── tests/
├── package.json
└── .env
```

---

## Next Steps

1. ✅ Complete quickstart setup
2. ⏭️ Read [spec.md](./spec.md) for feature requirements
3. ⏭️ Review [data-model.md](./data-model.md) for database schema
4. ⏭️ Check [plan.md](./plan.md) for architecture decisions
5. ⏭️ Run `/speckit.tasks` to generate implementation tasks
6. ⏭️ Start implementing with `/speckit.implement`

---

**Quickstart Guide Status**: ✅ **COMPLETE**
