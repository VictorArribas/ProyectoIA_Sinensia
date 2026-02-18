# ProyectoIA_Sinensia - Smart AI Gym Coach

Coach deportivo inteligente mediante LLMs. Proyecto para el Curso de IA y ML de Sinensia.

## Overview

Sistema de entrenamiento personalizado basado en LLM (Anthropic Claude) que:
- Genera planes de entrenamiento adaptados a tu perfil
- Gestiona la fatiga y recuperación de forma inteligente
- Calcula macros nutricionales automáticamente
- Ofrece consultoría técnica sobre ejercicios

## Quick Start

Ver **[quickstart.md](./quickstart.md)** para instrucciones detalladas de setup y uso.

### Docker (Recomendado)

```bash
# 1. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env y añadir tu ANTHROPIC_API_KEY

# 2. Levantar servicios
docker-compose up -d

# 3. Inicializar base de datos
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_exercises.py

# 4. Acceder
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI 0.104+, SQLAlchemy 2.0+ (async)
- **Frontend**: React 18+, Vite 5+, React Router v6
- **Database**: PostgreSQL 15+ with JSONB support
- **AI**: Anthropic Claude 3.5 Sonnet API
- **Auth**: JWT tokens (HS256, bcrypt)

## Project Structure

```
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Config, security, dependencies
│   │   └── middleware/ # Auth, CORS, rate limiting
│   ├── tests/
│   ├── scripts/       # Seed data, migrations
│   └── alembic/       # Database migrations
├── frontend/          # React + Vite application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/  # API client
│   │   ├── context/   # Global state
│   │   └── utils/
│   └── public/
└── specs/             # Feature specifications (Speckit)
    └── 001-ai-gym-coach/
        ├── spec.md    # Requirements
        ├── plan.md    # Architecture
        └── tasks.md   # Implementation tasks
```

## Documentation

- **[Quickstart Guide](./quickstart.md)** - Setup and usage instructions
- **[Feature Spec](./specs/001-ai-gym-coach/spec.md)** - Requirements and user stories
- **[Implementation Plan](./specs/001-ai-gym-coach/plan.md)** - Architecture and design
- **[API Contracts](./specs/001-ai-gym-coach/contracts/README.md)** - REST API documentation
- **[Data Model](./specs/001-ai-gym-coach/data-model.md)** - Database schema

## Development

### Running Tests

```bash
# Backend
docker-compose exec backend pytest

# Frontend
docker-compose exec frontend npm test
```

### Database Migrations

```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

## Constitution & Principles

This project follows principles defined in `.specify/memory/constitution.md`:

1. **Safety First**: Medical disclaimer, never diagnose injuries
2. **Scientific Foundation**: Evidence-based recommendations only
3. **Data Privacy**: GDPR compliance, user data ownership
4. **Progressive Overload**: Gradual, sustainable progression
5. **Recovery-Aware**: Fatigue management and deload weeks
6. **Technical Clarity**: Clear Pydantic schemas for LLM responses

## Contributing

1. Create feature branch: `git checkout -b 002-feature-name`
2. Follow Speckit workflow: `/specify` → `/clarify` → `/plan` → `/tasks` → `/implement`
3. Run tests: `pytest` (backend) and `npm test` (frontend)
4. Commit and push: `git commit -m "Description"`
5. Create Pull Request

## Disclaimer

⚠️ **Este sistema NO sustituye el consejo médico profesional**. Consulta con un médico antes de comenzar cualquier programa de ejercicio. Detente inmediatamente si experimentas dolor.

## License

Educational project for Sinensia AI & ML Course.
