# Setup Instructions - Smart AI Gym Coach MVP

## ✅ Estado Actual

**MVP Foundation (Fase 1 + Fase 2) - COMPLETADO**

- ✅ Backend FastAPI con autenticación JWT
- ✅ Frontend React con Vite
- ✅ PostgreSQL database schema (7 modelos)
- ✅ Docker Compose configurado
- ✅ 30 ejercicios en español listos para seed

---

## 🚀 Pasos para Levantar el Proyecto

### 1. Configurar Variables de Entorno

**Backend:**
```bash
cp backend/.env.example backend/.env
```

Editar `backend/.env` y añadir tu API Key de Anthropic:
```env
ANTHROPIC_API_KEY=sk-ant-api03-tu-clave-aqui
```

**Frontend:**
```bash
cp frontend/.env.example frontend/.env
```

No es necesario editar el archivo frontend/.env (usa valores por defecto).

---

### 2. Levantar Servicios con Docker

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

Esto levanta:
- **PostgreSQL** (puerto 5432)
- **Backend** (puerto 8000)
- **Frontend** (puerto 5173)

---

### 3. Inicializar Base de Datos

**Opción A: Comando único (recomendado)**

```bash
docker-compose exec backend bash -c "alembic upgrade head && python scripts/seed_exercises.py"
```

**Opción B: Paso por paso**

```bash
# Generar migración inicial
docker-compose exec backend alembic revision --autogenerate -m "Initial schema"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head

# Seed de ejercicios (30 ejercicios en español)
docker-compose exec backend python scripts/seed_exercises.py
```

---

### 4. Acceder a la Aplicación

- 🌐 **Frontend**: http://localhost:5173
- 📚 **API Docs (Swagger)**: http://localhost:8000/docs
- 🔧 **ReDoc**: http://localhost:8000/redoc
- 🗄️ **PostgreSQL**: localhost:5432 (user: postgres, pass: postgres, db: gym_coach_db)

---

## 🧪 Probar la API

### Registrar Usuario

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Endpoint Protegido (ejemplo)

```bash
# Guardar token
TOKEN="tu-access-token-aqui"

# Llamar endpoint protegido
curl http://localhost:8000/api/v1/protected \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Comandos Útiles

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Reiniciar Servicios

```bash
# Reiniciar todo
docker-compose restart

# Reiniciar solo backend
docker-compose restart backend
```

### Acceder a Contenedores

```bash
# Backend
docker-compose exec backend bash

# PostgreSQL
docker-compose exec db psql -U postgres -d gym_coach_db
```

### Migraciones de Base de Datos

```bash
# Ver estado de migraciones
docker-compose exec backend alembic current

# Crear nueva migración
docker-compose exec backend alembic revision --autogenerate -m "Add new table"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head

# Rollback última migración
docker-compose exec backend alembic downgrade -1
```

### Detener y Limpiar

```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (¡PIERDE DATOS!)
docker-compose down -v

# Rebuild completo
docker-compose up -d --build
```

---

## 📊 Estado de Implementación

### ✅ Fase 1: Setup (10/10)
- Estructura de directorios
- Docker Compose
- Backend FastAPI
- Frontend React + Vite
- Alembic configurado

### ✅ Fase 2: Foundational (16/16)
- 7 modelos SQLAlchemy
- Autenticación JWT completa
- Rate limiting (5 intentos/15min login)
- 30 ejercicios en seed script
- Frontend auth context (AuthProvider, useAuth)

### ⏳ Próximas Fases
- **Fase 3 (US1)**: Generación de planes de entrenamiento con Claude AI
- **Fase 4 (US2)**: Sistema de gestión de fatiga
- **Fase 5 (US3)**: Calculadora de nutrición
- **Fase 6 (US4)**: Chat de consultoría técnica

---

## 🐛 Troubleshooting

### Error: "Cannot connect to database"

**Solución:**
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart
```

### Error: "Invalid API key" (Anthropic)

**Solución:**
1. Verificar que `backend/.env` contiene `ANTHROPIC_API_KEY=sk-ant-api03-...`
2. Obtener una API key válida en https://console.anthropic.com/
3. Reiniciar backend: `docker-compose restart backend`

### Frontend: "CORS policy error"

**Solución:**
1. Verificar que backend está en http://localhost:8000
2. Verificar `frontend/.env` tiene `VITE_API_BASE_URL=http://localhost:8000/api/v1`
3. Reiniciar frontend: `docker-compose restart frontend`

### Migraciones fallan

**Solución:**
```bash
# Ver estado
docker-compose exec backend alembic current

# Forzar upgrade
docker-compose exec backend alembic upgrade head

# Si persiste, resetear DB (PIERDE DATOS)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_exercises.py
```

---

## 📚 Documentación Adicional

- **Quickstart completo**: [quickstart.md](./quickstart.md)
- **Especificación**: [specs/001-ai-gym-coach/spec.md](./specs/001-ai-gym-coach/spec.md)
- **Plan de implementación**: [specs/001-ai-gym-coach/plan.md](./specs/001-ai-gym-coach/plan.md)
- **Tareas**: [specs/001-ai-gym-coach/tasks.md](./specs/001-ai-gym-coach/tasks.md)
- **Modelo de datos**: [specs/001-ai-gym-coach/data-model.md](./specs/001-ai-gym-coach/data-model.md)
- **Contratos API**: [specs/001-ai-gym-coach/contracts/](./specs/001-ai-gym-coach/contracts/)

---

## 🎯 Siguiente Paso

Una vez que los servicios estén corriendo y la base de datos inicializada, puedes:

1. **Probar el frontend**: http://localhost:5173
2. **Explorar la API**: http://localhost:8000/docs
3. **Continuar con Fase 3 (US1)**: Implementar generación de planes de entrenamiento con Claude

---

**¡Listo! 🎉** Tu MVP Foundation está completamente configurado.
