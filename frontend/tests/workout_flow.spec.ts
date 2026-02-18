/**
 * workout_flow.spec.ts
 *
 * Test E2E que simula el flujo completo de un usuario nuevo:
 *   1. Registro de cuenta
 *   2. Rellenado del perfil (peso, altura, edad)
 *   3. Pulsación del botón "Generar Plan de Entrenamiento"
 *   4. Verificación de que aparece la respuesta del LLM en pantalla
 *
 * Todos los endpoints del backend están MOCKEADOS con page.route(),
 * por lo que el test funciona sin necesitar el servidor FastAPI ni Claude AI.
 */

import { test, expect, type Page } from '@playwright/test'

// ──────────────────────────────────────────────────────────────────────────────
// Datos de mock: simulan exactamente lo que devolvería el backend + LLM
// ──────────────────────────────────────────────────────────────────────────────

/** Un ejercicio de ejemplo que "genera el LLM" */
const MOCK_EXERCISE = {
  musculo: 'Pecho',
  ejercicio: 'Press de banca con mancuernas',
  series: 4,
  repeticiones: '8-10',
  rpe_objetivo: 8,
  descanso_segundos: 90,
  notas_seguridad: 'Mantén la espalda plana durante todo el movimiento.',
}

/** Respuesta completa que devuelve POST /workouts/generate (simula el LLM) */
const MOCK_WORKOUT_RESPONSE = {
  fatiga_score_usado: 50,
  ajuste_aplicado: null,
  workout_plan: [MOCK_EXERCISE],
  disclaimer_medico:
    'Consulta siempre con un profesional de la salud antes de comenzar cualquier plan de entrenamiento.',
}

// ──────────────────────────────────────────────────────────────────────────────
// Interceptores de red
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Registra todos los mocks de red necesarios para el flujo completo.
 * Usa la variable 'profileCreated' para simular el cambio de estado
 * entre "perfil no existe (404)" y "perfil ya creado (200)".
 */
async function mockBackend(page: Page): Promise<void> {
  // ── Auth ──────────────────────────────────────────────────────────────────
  // POST /auth/register → devuelve tokens JWT falsos
  await page.route('**/api/v1/auth/register', (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        access_token: 'fake-access-token',
        refresh_token: 'fake-refresh-token',
      }),
    }),
  )

  // ── Perfil ─────────────────────────────────────────────────────────────────
  // GET /profile/me → 404 antes de crear el perfil; 200 después
  let profileCreated = false

  await page.route('**/api/v1/profile/me', (route) => {
    if (!profileCreated) {
      return route.fulfill({
        status: 404,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Profile not found' }),
      })
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        age: 28,
        weight_kg: 75.0,
        height_cm: 178.0,
        objective: 'hypertrophy',
        experience_level: 'beginner',
        training_days_per_week: 3,
        equipment_available: ['dumbbells', 'barbell', 'bodyweight'],
        // injury_history: campo guardado en backend pero sin UI todavía
        injury_history: [],
      }),
    })
  })

  // POST /profile/create → crea el perfil y activa la bandera
  await page.route('**/api/v1/profile/create', (route) => {
    profileCreated = true
    return route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({ id: 1, age: 28, weight_kg: 75.0, height_cm: 178.0 }),
    })
  })

  // ── Entrenamientos ─────────────────────────────────────────────────────────
  // GET /workouts/history → historial vacío (usuario nuevo)
  await page.route('**/api/v1/workouts/history', (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([]),
    }),
  )

  // POST /workouts/generate → plan generado por el LLM (mockeado)
  await page.route('**/api/v1/workouts/generate', (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_WORKOUT_RESPONSE),
    }),
  )
}

// ──────────────────────────────────────────────────────────────────────────────
// Test principal
// ──────────────────────────────────────────────────────────────────────────────

test('flujo completo: registro → perfil → generar rutina', async ({ page }) => {
  // La app usa window.alert() en varios puntos.
  // Este listener los acepta automáticamente para no bloquear el test.
  page.on('dialog', (dialog) => dialog.accept())

  // Instalar todos los mocks ANTES de la primera navegación
  await mockBackend(page)

  // ─── PASO 1: Registro ─────────────────────────────────────────────────────
  await page.goto('/register')

  await expect(page.getByRole('heading', { name: 'Registrarse' })).toBeVisible()

  await page.getByPlaceholder('tu@email.com').fill('alumno@gimnasio.com')
  await page.getByPlaceholder('Mínimo 8 caracteres').fill('Password123')
  await page.getByPlaceholder('Repite tu contraseña').fill('Password123')

  await page.getByRole('button', { name: 'Crear Cuenta' }).click()

  // Tras el registro, la app muestra un alert y redirige a /profile
  await expect(page).toHaveURL('/profile')

  // ─── PASO 2: Rellenar perfil (peso, altura, lesiones) ─────────────────────
  await expect(page.getByRole('heading', { name: 'Crear Perfil' })).toBeVisible()

  // Los inputs del ProfileForm NO tienen atributo 'for' en sus labels,
  // así que los seleccionamos por el atributo 'name' del input.
  await page.locator('input[name="age"]').fill('28')
  await page.locator('input[name="weight_kg"]').fill('75')
  await page.locator('input[name="height_cm"]').fill('178')

  // ── Lesiones ──
  // El campo 'injury_history' existe en el modelo de datos del backend
  // pero la interfaz actual (ProfileForm.jsx) aún no lo expone como input.
  // Cuando se añada el campo al formulario, descomenta y adapta esta línea:
  //
  //   await page.locator('input[name="injury_history"]')
  //     .fill('Tendinitis crónica en rodilla izquierda')
  //
  // Por ahora el backend recibe injury_history: [] (array vacío por defecto).

  await page.getByRole('button', { name: 'Crear Perfil' }).click()

  // Tras crear el perfil, la app muestra un alert y redirige a /workouts
  await expect(page).toHaveURL('/workouts')

  // ─── PASO 3: Pulsar el botón "Generar Rutina" ─────────────────────────────
  await expect(
    page.getByRole('heading', { name: 'Planes de Entrenamiento' }),
  ).toBeVisible()

  // El botón dice "🤖 Generar Plan de Entrenamiento" → usamos regex parcial
  await page.getByRole('button', { name: /Generar Plan de Entrenamiento/i }).click()

  // ─── PASO 4: Verificar que aparece texto en pantalla (respuesta del LLM) ──

  // 4a. Aparece el encabezado de la sección generada
  await expect(
    page.getByRole('heading', { name: 'Tu Plan de Entrenamiento' }),
  ).toBeVisible()

  // 4b. La tabla muestra el nombre del ejercicio que devolvió el LLM
  await expect(page.getByText('Press de banca con mancuernas')).toBeVisible()

  // 4c. El disclaimer médico confirma que todo el JSON del LLM se renderizó
  await expect(
    page.getByText(/Consulta siempre con un profesional de la salud/i),
  ).toBeVisible()
})
