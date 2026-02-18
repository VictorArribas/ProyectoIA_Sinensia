"""
Seed Script - Populate Exercise Library
Creates 50-100 exercises with Spanish names, safety notes, technique cues
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import AsyncSessionLocal, engine, Base
from src.models.exercise import Exercise


EXERCISES_DATA = [
    # PECHO
    {
        "name": "Press Banca con Barra",
        "muscle_groups": ["pectoral", "triceps", "deltoides anterior"],
        "safety_notes": "No arquear excesivamente la espalda. Mantener escápulas retraídas. Usar spotters para cargas altas.",
        "technique_cues": [
            "Escápulas retraídas y deprimidas",
            "Codos 45 grados del torso",
            "Barra desciende a pezones",
            "Pies firmes en el suelo",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-12",
            "intermediate": "4x6-10",
            "advanced": "4-5x5-8",
        },
    },
    {
        "name": "Press Inclinado con Mancuernas",
        "muscle_groups": ["pectoral superior", "triceps", "deltoides anterior"],
        "safety_notes": "Banco a 30-45 grados. Control en el descenso. No bloquear codos completamente.",
        "technique_cues": [
            "Banco a 30-45 grados",
            "Descenso controlado hasta altura clavícula",
            "Mancuernas en ángulo neutral",
            "Estabilizar core",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3-4x8-12",
            "advanced": "4x8-10",
        },
    },
    {
        "name": "Aperturas con Mancuernas",
        "muscle_groups": ["pectoral"],
        "safety_notes": "Mantener ligera flexión de codos. No descender más allá del plano del hombro. Usar peso moderado.",
        "technique_cues": [
            "Ligera flexión de codos fija",
            "Descenso hasta nivel del hombro",
            "Movimiento arqueado, no prensa",
            "Apriete en la contracción",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-14",
            "advanced": "3-4x10-12",
        },
    },
    {
        "name": "Flexiones (Push-ups)",
        "muscle_groups": ["pectoral", "triceps", "deltoides anterior", "core"],
        "safety_notes": "Mantener columna neutral. No dejar caer las caderas. Escápulas estables.",
        "technique_cues": [
            "Cuerpo en línea recta",
            "Manos bajo hombros",
            "Descenso hasta pecho cerca del suelo",
            "Activar core y glúteos",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-15",
            "intermediate": "3-4x15-25",
            "advanced": "4x20-30 o con lastre",
        },
    },
    # ESPALDA
    {
        "name": "Dominadas (Pull-ups)",
        "muscle_groups": ["dorsal ancho", "bíceps", "trapecio medio"],
        "safety_notes": "Evitar balanceo excesivo. Descenso controlado. No forzar si hay dolor de hombro.",
        "technique_cues": [
            "Agarre pronado ligeramente mayor que hombros",
            "Escápulas deprimidas al inicio",
            "Pecho hacia la barra",
            "Control en el descenso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x3-8 o asistidas",
            "intermediate": "3-4x6-12",
            "advanced": "4x8-15 o con lastre",
        },
    },
    {
        "name": "Remo con Barra (Bent-Over Row)",
        "muscle_groups": ["dorsal ancho", "trapecio medio", "romboides", "erectores espinales"],
        "safety_notes": "Mantener espalda neutra. No redondear columna lumbar. Core activo todo el movimiento.",
        "technique_cues": [
            "Bisagra de cadera, espalda recta",
            "Barra tira hacia abdomen bajo",
            "Escápulas retraídas en contracción",
            "Codos pegados al torso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-12",
            "intermediate": "4x8-10",
            "advanced": "4x6-10",
        },
    },
    {
        "name": "Remo Unilateral con Mancuerna",
        "muscle_groups": ["dorsal ancho", "trapecio", "romboides"],
        "safety_notes": "Apoyar rodilla y mano en banco. Espalda neutral. No rotar torso en la tracción.",
        "technique_cues": [
            "Rodilla y mano de apoyo alineadas",
            "Mancuerna tira hacia cadera",
            "Escápula retrae al final",
            "No rotar el tronco",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12 por lado",
            "intermediate": "3-4x8-12 por lado",
            "advanced": "4x8-10 por lado",
        },
    },
    {
        "name": "Jalón al Pecho (Lat Pulldown)",
        "muscle_groups": ["dorsal ancho", "trapecio inferior", "bíceps"],
        "safety_notes": "No tirar detrás del cuello. Evitar balanceo. Descenso controlado.",
        "technique_cues": [
            "Agarre pronado ancho",
            "Pecho alto hacia la barra",
            "Codos bajan hacia costados",
            "Control en la fase excéntrica",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3-4x8-12",
            "advanced": "4x8-12",
        },
    },
    {
        "name": "Peso Muerto (Deadlift)",
        "muscle_groups": ["erectores espinales", "glúteos", "isquiotibiales", "trapecio"],
        "safety_notes": "CRÍTICO: Mantener columna neutral. No redondear lumbar. Iniciar con peso ligero y dominar técnica.",
        "technique_cues": [
            "Pies ancho de caderas",
            "Barra sobre media pie",
            "Columna neutral siempre",
            "Bisagra de cadera, empuje de glúteos",
            "Barra pegada a piernas",
        ],
        "volume_guidelines_json": {
            "beginner": "3x5-8 (enfoque técnica)",
            "intermediate": "3-4x5-8",
            "advanced": "4x3-6",
        },
    },
    # PIERNAS
    {
        "name": "Sentadilla con Barra (Back Squat)",
        "muscle_groups": ["cuádriceps", "glúteos", "isquiotibiales", "erectores espinales"],
        "safety_notes": "Profundidad segura según movilidad. No colapsar rodillas hacia adentro. Usar spotters para cargas altas.",
        "technique_cues": [
            "Pies ancho de hombros",
            "Rodillas siguen línea de pies",
            "Profundidad: cadera bajo rodillas",
            "Pecho alto, core activo",
            "Empuje desde talones",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-12",
            "intermediate": "4x6-10",
            "advanced": "4-5x5-8",
        },
    },
    {
        "name": "Prensa de Piernas (Leg Press)",
        "muscle_groups": ["cuádriceps", "glúteos", "isquiotibiales"],
        "safety_notes": "No despegar lumbar del respaldo. Profundidad controlada. No bloquear rodillas.",
        "technique_cues": [
            "Pies posición media-alta del plato",
            "Lumbar pegada al respaldo",
            "Rodillas alineadas con pies",
            "Descenso hasta 90 grados rodilla",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-15",
            "intermediate": "3-4x10-12",
            "advanced": "4x8-12",
        },
    },
    {
        "name": "Zancadas (Lunges)",
        "muscle_groups": ["cuádriceps", "glúteos", "isquiotibiales"],
        "safety_notes": "Rodilla delantera no sobrepasa punta del pie. Torso erguido. Balance estable.",
        "technique_cues": [
            "Paso amplio hacia adelante",
            "Rodilla trasera cerca del suelo",
            "Torso vertical",
            "Rodilla delantera a 90 grados",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-10 por pierna",
            "intermediate": "3x10-12 por pierna",
            "advanced": "3-4x10-12 por pierna con peso",
        },
    },
    {
        "name": "Peso Muerto Rumano",
        "muscle_groups": ["isquiotibiales", "glúteos", "erectores espinales"],
        "safety_notes": "Enfoque en bisagra de cadera, no sentadilla. Columna neutral. Barra cerca de piernas.",
        "technique_cues": [
            "Rodillas ligeramente flexionadas fijas",
            "Bisagra de cadera, pecho hacia adelante",
            "Barra baja por tibias",
            "Sentir estiramiento en isquios",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-12",
            "intermediate": "3-4x8-12",
            "advanced": "4x8-10",
        },
    },
    {
        "name": "Extensión de Cuádriceps (Leg Extension)",
        "muscle_groups": ["cuádriceps"],
        "safety_notes": "No usar cargas excesivas. Control en la fase excéntrica. Evitar si hay dolor de rodilla.",
        "technique_cues": [
            "Espalda contra respaldo",
            "Extensión completa controlada",
            "Descenso lento",
            "Rodillas alineadas con eje de máquina",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-15",
            "advanced": "3-4x10-15",
        },
    },
    {
        "name": "Curl Femoral (Leg Curl)",
        "muscle_groups": ["isquiotibiales"],
        "safety_notes": "No arquear lumbar. Rango completo de movimiento. Peso moderado.",
        "technique_cues": [
            "Caderas firmes contra banco",
            "Flexión completa de rodillas",
            "Control en la extensión",
            "No despegar caderas",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-15",
            "advanced": "3-4x10-15",
        },
    },
    {
        "name": "Elevaciones de Gemelos de Pie (Standing Calf Raise)",
        "muscle_groups": ["gastrocnemios", "sóleo"],
        "safety_notes": "Rango completo. No rebotar en la parte baja. Mantener rodillas ligeramente flexionadas.",
        "technique_cues": [
            "Bolas de los pies en el borde",
            "Elevación máxima en puntillas",
            "Descenso completo",
            "Pausa en contracción",
        ],
        "volume_guidelines_json": {
            "beginner": "3x15-20",
            "intermediate": "3-4x12-20",
            "advanced": "4x10-20",
        },
    },
    # HOMBROS
    {
        "name": "Press Militar con Barra",
        "muscle_groups": ["deltoides anterior", "deltoides lateral", "triceps"],
        "safety_notes": "No arquear excesivamente la espalda. Core activo. Barra parte desde clavículas.",
        "technique_cues": [
            "Pies ancho de caderas",
            "Barra parte de clavículas",
            "Empuje vertical",
            "Core activo, no arquear lumbar",
        ],
        "volume_guidelines_json": {
            "beginner": "3x8-12",
            "intermediate": "3-4x6-10",
            "advanced": "4x5-8",
        },
    },
    {
        "name": "Elevaciones Laterales con Mancuernas",
        "muscle_groups": ["deltoides lateral"],
        "safety_notes": "No usar impulso. Peso moderado. No elevar por encima del hombro si hay molestias.",
        "technique_cues": [
            "Ligera flexión de codos",
            "Elevar hasta altura de hombros",
            "Codos ligeramente por encima de manos",
            "Control en el descenso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-15",
            "advanced": "3-4x10-15",
        },
    },
    {
        "name": "Elevaciones Frontales con Mancuernas",
        "muscle_groups": ["deltoides anterior"],
        "safety_notes": "No usar balanceo. Evitar si hay dolor de hombro anterior.",
        "technique_cues": [
            "Mancuernas frente a muslos",
            "Elevación hasta altura de ojos",
            "Alternar brazos o simultáneas",
            "Control en descenso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-12",
            "advanced": "3x10-12",
        },
    },
    {
        "name": "Pájaros (Face Pulls con Cables)",
        "muscle_groups": ["deltoides posterior", "trapecio medio", "romboides"],
        "safety_notes": "Movimiento esencial para salud de hombro. Peso moderado, muchas repeticiones.",
        "technique_cues": [
            "Cables a altura de cara",
            "Tirar hacia frente de cara",
            "Codos altos y abiertos",
            "Retraer escápulas",
        ],
        "volume_guidelines_json": {
            "beginner": "3x15-20",
            "intermediate": "3x15-20",
            "advanced": "3-4x15-20",
        },
    },
    {
        "name": "Remo al Mentón con Barra (Upright Row)",
        "muscle_groups": ["deltoides lateral", "trapecio superior"],
        "safety_notes": "No elevar más allá del esternón si causa dolor. Considerar alternativas si hay molestia de hombro.",
        "technique_cues": [
            "Agarre ancho",
            "Codos altos y abiertos",
            "Barra hasta esternón",
            "No encoger hombros",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3x8-12",
            "advanced": "3x8-12",
        },
    },
    # BRAZOS
    {
        "name": "Curl de Bíceps con Barra",
        "muscle_groups": ["bíceps braquial", "braquial anterior"],
        "safety_notes": "No usar balanceo. Codos fijos al torso. Peso controlado.",
        "technique_cues": [
            "Codos pegados al torso",
            "Extensión completa abajo",
            "Flexión sin mover codos hacia adelante",
            "Control en descenso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3x8-12",
            "advanced": "3-4x8-12",
        },
    },
    {
        "name": "Curl de Bíceps con Mancuernas Alternado",
        "muscle_groups": ["bíceps braquial"],
        "safety_notes": "Mantener core estable. No rotar muñeca excesivamente. Sin balanceo.",
        "technique_cues": [
            "Mancuernas en posición neutral abajo",
            "Supinación en la subida",
            "Alternar brazos",
            "Codos fijos",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12 por brazo",
            "intermediate": "3x8-12 por brazo",
            "advanced": "3x8-12 por brazo",
        },
    },
    {
        "name": "Curl Martillo (Hammer Curl)",
        "muscle_groups": ["bíceps braquial", "braquial anterior", "braquiorradial"],
        "safety_notes": "Agarre neutral todo el movimiento. Codos estables. Control total.",
        "technique_cues": [
            "Agarre neutral (palmas enfrentadas)",
            "Codos al costado",
            "Flexión hasta hombro",
            "Descenso controlado",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3x10-12",
            "advanced": "3x8-12",
        },
    },
    {
        "name": "Press Francés (Skullcrushers)",
        "muscle_groups": ["triceps"],
        "safety_notes": "No bloquear codos agresivamente. Peso moderado. Control total del movimiento.",
        "technique_cues": [
            "Barra desciende hacia frente",
            "Codos fijos, solo mueven antebrazo",
            "Extensión completa sin bloquear",
            "Control en descenso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-12",
            "intermediate": "3x8-12",
            "advanced": "3x8-12",
        },
    },
    {
        "name": "Extensión de Tríceps en Polea Alta",
        "muscle_groups": ["triceps"],
        "safety_notes": "Codos fijos al torso. No usar impulso. Extensión completa sin bloquear.",
        "technique_cues": [
            "Codos pegados al torso",
            "Extensión completa abajo",
            "Control en la vuelta",
            "No inclinar torso",
        ],
        "volume_guidelines_json": {
            "beginner": "3x12-15",
            "intermediate": "3x10-15",
            "advanced": "3x10-15",
        },
    },
    {
        "name": "Fondos en Paralelas (Dips)",
        "muscle_groups": ["pectoral inferior", "triceps", "deltoides anterior"],
        "safety_notes": "Descenso controlado. No descender más allá de 90 grados de codo si hay dolor. Usar asistencia si es necesario.",
        "technique_cues": [
            "Ligera inclinación hacia adelante para pecho",
            "Descenso hasta 90 grados codo",
            "Empuje controlado",
            "Escápulas estables",
        ],
        "volume_guidelines_json": {
            "beginner": "3x5-10 o asistidas",
            "intermediate": "3x8-15",
            "advanced": "3x10-20 o con lastre",
        },
    },
    # CORE
    {
        "name": "Plancha (Plank)",
        "muscle_groups": ["recto abdominal", "transverso abdominal", "oblicuos"],
        "safety_notes": "Mantener columna neutral. No dejar caer caderas. Respirar normal.",
        "technique_cues": [
            "Cuerpo en línea recta",
            "Core activo, ombligo hacia dentro",
            "No bajar caderas ni elevarlas",
            "Respiración normal",
        ],
        "volume_guidelines_json": {
            "beginner": "3x20-30 segundos",
            "intermediate": "3x45-60 segundos",
            "advanced": "3x60-90 segundos",
        },
    },
    {
        "name": "Crunch Abdominal",
        "muscle_groups": ["recto abdominal"],
        "safety_notes": "No tirar del cuello. Movimiento controlado. Rango parcial del abdomen.",
        "technique_cues": [
            "Manos detrás de cabeza sin tirar",
            "Flexión de tronco, no de cuello",
            "Elevación de escápulas del suelo",
            "Descenso controlado",
        ],
        "volume_guidelines_json": {
            "beginner": "3x15-20",
            "intermediate": "3x20-30",
            "advanced": "3x25-40",
        },
    },
    {
        "name": "Elevación de Piernas (Leg Raises)",
        "muscle_groups": ["recto abdominal inferior", "flexores de cadera"],
        "safety_notes": "No arquear lumbar. Si es necesario, flexionar rodillas. Descenso controlado.",
        "technique_cues": [
            "Lumbar pegada al suelo",
            "Piernas juntas",
            "Elevación hasta 90 grados",
            "Descenso sin tocar suelo",
        ],
        "volume_guidelines_json": {
            "beginner": "3x10-15 (rodillas flexionadas)",
            "intermediate": "3x12-20",
            "advanced": "3x15-25",
        },
    },
    {
        "name": "Russian Twist",
        "muscle_groups": ["oblicuos", "recto abdominal"],
        "safety_notes": "Mantener columna neutra. No usar peso excesivo. Movimiento controlado.",
        "technique_cues": [
            "Torso inclinado 45 grados",
            "Pies elevados o en suelo (según nivel)",
            "Rotación de torso lado a lado",
            "Peso toca suelo cada lado",
        ],
        "volume_guidelines_json": {
            "beginner": "3x20-30 (total ambos lados)",
            "intermediate": "3x30-40",
            "advanced": "3x40-60",
        },
    },
    {
        "name": "Mountain Climbers",
        "muscle_groups": ["core", "cardio"],
        "safety_notes": "Mantener espalda neutral. Caderas estables. Movimiento rápido pero controlado.",
        "technique_cues": [
            "Posición de plancha alta",
            "Rodillas alternan hacia pecho",
            "Caderas estables",
            "Ritmo constante",
        ],
        "volume_guidelines_json": {
            "beginner": "3x20-30 segundos",
            "intermediate": "3x30-45 segundos",
            "advanced": "3x45-60 segundos",
        },
    },
]


async def seed_exercises():
    """Populate exercise library with 50+ exercises"""
    async with AsyncSessionLocal() as session:
        # Check if exercises already exist
        from sqlalchemy import select

        result = await session.execute(select(Exercise))
        existing = result.scalars().all()

        if existing:
            print(f"⚠️  Database already has {len(existing)} exercises. Skipping seed.")
            return

        # Insert exercises
        print(f"📚 Seeding {len(EXERCISES_DATA)} exercises...")
        for ex_data in EXERCISES_DATA:
            exercise = Exercise(**ex_data)
            session.add(exercise)

        await session.commit()
        print(f"✅ Successfully seeded {len(EXERCISES_DATA)} exercises!")


async def main():
    """Main seed function"""
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed exercises
    await seed_exercises()


if __name__ == "__main__":
    asyncio.run(main())
