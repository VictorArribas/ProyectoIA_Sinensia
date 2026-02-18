# Quickstart: Smart AI Gym Coach

Guía rápida para levantar y utilizar el proyecto **ProyectoIA_Sinensia** - Coach deportivo inteligente con LLMs.

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **Git** - Para clonar el repositorio
- **Docker Desktop** - [Descargar aquí](https://www.docker.com/products/docker-desktop/)
- **Una API Key de Anthropic Claude** - [Obtener aquí](https://console.anthropic.com/)

**Alternativa sin Docker**:
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

---

## 🚀 Inicio Rápido (Recomendado - Docker)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/your-org/ProyectoIA_Sinensia.git
cd ProyectoIA_Sinensia
```

### 2. Configurar Variables de Entorno

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

**Edita `backend/.env`** y añade tu API Key de Anthropic:

```env
ANTHROPIC_API_KEY=sk-ant-api03-tu-clave-aqui
```

### 3. Levantar los Servicios

```bash
docker-compose up -d
```

Esto inicia:
- **PostgreSQL** (base de datos) - Puerto 5432
- **Backend (FastAPI)** - Puerto 8000
- **Frontend (React + Vite)** - Puerto 5173

### 4. Inicializar la Base de Datos

```bash
# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Cargar ejercicios de ejemplo (50-100 ejercicios)
docker-compose exec backend python scripts/seed_exercises.py
```

### 5. Acceder a la Aplicación

🌐 **Frontend**: [http://localhost:5173](http://localhost:5173)
📚 **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
🔧 **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎯 Cómo Usar el Sistema

### Primer Uso: Crear tu Cuenta y Perfil

1. **Abrir el frontend**: [http://localhost:5173](http://localhost:5173)
2. **Registrarse**:
   - Click en "Registrarse"
   - Introduce tu email y contraseña
   - Click "Crear cuenta"

3. **Completar tu Perfil**:
   - Edad, peso, altura
   - Objetivo: Hipertrofia / Definición / Fuerza / Recomposición
   - Nivel de experiencia: Principiante / Intermedio / Avanzado
   - Días de entrenamiento por semana
   - Equipamiento disponible (mancuernas, barra, cables, etc.)
   - Lesiones actuales (opcional)

4. **Generar tu Primer Plan de Entrenamiento**:
   - Navegar a "Entrenamientos"
   - Click "Generar Plan de Entrenamiento"
   - ⏳ El sistema consulta a Claude AI (tarda 5-10 segundos)
   - ✅ Verás tu rutina personalizada en tabla:
     - Ejercicio
     - Músculo trabajado
     - Series y repeticiones
     - RPE objetivo (intensidad)
     - Descanso entre series
     - Notas de seguridad

### Funcionalidades Principales

#### 1️⃣ **Gestión de Fatiga Inteligente**

Después de cada entrenamiento:
- **Registra tu sesión**:
  - RPE (1-10): ¿Qué tan duro fue el entreno?
  - ¿Sentiste dolor? → Sí/No
  - Ubicación del dolor (si aplica)

El sistema ajusta automáticamente tu próxima rutina:
- **RPE alto (9-10) o dolor** → Reduce volumen 20-30%
- **3+ entrenamientos con RPE 8+** → Sugiere semana de descarga (50% volumen)
- **RPE bajo (3-5) durante 2 semanas** → Aumenta intensidad 5-10%

#### 2️⃣ **Calculadora de Nutrición**

- Navegar a "Nutrición"
- El sistema calcula automáticamente:
  - **TDEE** (Gasto Energético Total Diario)
  - **Calorías objetivo** (según tu objetivo)
  - **Macros**: Proteínas, carbohidratos, grasas (en gramos)
- **Auto-actualiza** cuando cambias tu peso

#### 3️⃣ **Chat de Consultoría Técnica**

- Navegar a "Consultoría"
- Pregunta:
  - ✅ "¿Cómo hago una sentadilla correcta?"
  - ✅ "No tengo máquina de cables, ¿qué alternativas hay?"
  - ✅ "¿Qué es la sobrecarga progresiva?"
- El sistema responde con:
  - Instrucciones paso a paso
  - Alternativas basadas en evidencia
  - Explicaciones en lenguaje simple

⚠️ **Importante**: El sistema **NO puede diagnosticar lesiones**. Si preguntas sobre dolor persistente, te recomendará consultar un médico.

---

## 🛑 Detener los Servicios

```bash
docker-compose down
```

Para **eliminar también los datos** (base de datos):
```bash
docker-compose down -v
```

---

## 🔧 Comandos Útiles

### Ver Logs

```bash
# Ver todos los logs
docker-compose logs -f

# Ver solo backend
docker-compose logs -f backend

# Ver solo frontend
docker-compose logs -f frontend
```

### Reiniciar un Servicio

```bash
# Reiniciar backend
docker-compose restart backend

# Reiniciar frontend
docker-compose restart frontend
```

### Acceder a la Base de Datos

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d gym_coach_db

# Ver tablas
\dt

# Salir
\q
```

### Ejecutar Tests

```bash
# Backend (pytest)
docker-compose exec backend pytest

# Frontend (Vitest)
docker-compose exec frontend npm test
```

---

## ⚙️ Setup Manual (Sin Docker)

<details>
<summary>Click aquí para instrucciones sin Docker</summary>

### Backend

```bash
cd backend

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tu API key y configuración de PostgreSQL

# Ejecutar migraciones
alembic upgrade head

# Seed ejercicios
python scripts/seed_exercises.py

# Iniciar servidor
uvicorn src.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar .env
cp .env.example .env
# Editar .env si necesitas cambiar la URL de la API

# Iniciar dev server
npm run dev
```

### PostgreSQL

```bash
# Instalar PostgreSQL 15+
# macOS: brew install postgresql@15
# Ubuntu: sudo apt install postgresql-15
# Windows: Descargar desde postgresql.org

# Crear base de datos
psql -U postgres
CREATE DATABASE gym_coach_db;
CREATE USER gym_coach_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE gym_coach_db TO gym_coach_user;
\q

# Actualizar backend/.env con:
DATABASE_URL=postgresql://gym_coach_user:tu_password@localhost:5432/gym_coach_db
```

</details>

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar a la base de datos"

**Causa**: PostgreSQL no está corriendo o las credenciales son incorrectas.

**Solución**:
```bash
# Verificar que Docker está corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart
```

### Error: "Invalid API key" (Anthropic)

**Causa**: Tu API Key de Anthropic no es válida o no está configurada.

**Solución**:
1. Verificar que `backend/.env` contiene `ANTHROPIC_API_KEY=sk-ant-api03-...`
2. Obtener una API key válida en [console.anthropic.com](https://console.anthropic.com/)
3. Reiniciar backend: `docker-compose restart backend`

### Error: "CORS policy" en Frontend

**Causa**: El backend no está corriendo o la URL de la API es incorrecta.

**Solución**:
1. Verificar que backend está en http://localhost:8000
2. Verificar `frontend/.env` tiene `VITE_API_BASE_URL=http://localhost:8000/api/v1`
3. Reiniciar frontend: `docker-compose restart frontend`

### Frontend: "Cannot GET /" o página en blanco

**Causa**: El frontend no compiló correctamente o hay un error de JavaScript.

**Solución**:
```bash
# Ver logs del frontend
docker-compose logs frontend

# Reconstruir frontend
docker-compose up -d --build frontend
```

### Backend: Migraciones fallan

**Causa**: Base de datos en estado inconsistente.

**Solución**:
```bash
# Ver estado de migraciones
docker-compose exec backend alembic current

# Forzar upgrade
docker-compose exec backend alembic upgrade head

# Si persiste, resetear base de datos (PIERDE DATOS)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_exercises.py
```

---

## 📚 Documentación Adicional

- **Especificación completa**: [specs/001-ai-gym-coach/spec.md](specs/001-ai-gym-coach/spec.md)
- **Plan de implementación**: [specs/001-ai-gym-coach/plan.md](specs/001-ai-gym-coach/plan.md)
- **Modelo de datos**: [specs/001-ai-gym-coach/data-model.md](specs/001-ai-gym-coach/data-model.md)
- **Contratos de API**: [specs/001-ai-gym-coach/contracts/](specs/001-ai-gym-coach/contracts/)
- **Guía de desarrollo**: [specs/001-ai-gym-coach/quickstart.md](specs/001-ai-gym-coach/quickstart.md)
- **Constitución del proyecto**: [.specify/memory/constitution.md](.specify/memory/constitution.md)

---

## 🤝 Contribuir

Este proyecto es parte del **Curso de IA y ML de Sinensia**. Para contribuir:

1. Crea un branch: `git checkout -b feature/mi-feature`
2. Haz tus cambios
3. Ejecuta tests: `pytest` (backend) y `npm test` (frontend)
4. Commit: `git commit -m "Descripción del cambio"`
5. Push: `git push origin feature/mi-feature`
6. Crea un Pull Request

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/your-org/ProyectoIA_Sinensia/issues)
- **Documentación técnica**: Carpeta `specs/001-ai-gym-coach/`
- **Preguntas sobre Speckit**: [CLAUDE.md](CLAUDE.md)

---

## ⚖️ Disclaimer Médico

⚠️ **Este sistema NO sustituye el consejo médico profesional**. Antes de comenzar cualquier programa de ejercicio:

- Consulta con un médico o profesional de la salud
- Detente inmediatamente si experimentas dolor
- El sistema recomienda consultar un profesional si reportas lesiones o dolor persistente

---

## 📄 Licencia

Este proyecto es educativo y parte del programa de IA y ML de Sinensia.

---

**¡Listo! 🎉** Ya puedes empezar a usar tu coach deportivo inteligente.

Si encuentras problemas, revisa la sección de **Solución de Problemas** o consulta los logs con `docker-compose logs -f`.
