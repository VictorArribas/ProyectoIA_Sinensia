import { defineConfig, devices } from '@playwright/test'

/**
 * Configuración de Playwright para tests E2E del AI Gym Coach.
 *
 * Documentación: https://playwright.dev/docs/test-configuration
 *
 * Comandos de ejecución:
 *   npx playwright test                  → modo headless (sin ventana)
 *   npx playwright test --headed         → modo headed (VER en pantalla) ← lo que quieres
 *   npx playwright test --headed --slow-mo=500  → headed + 500ms entre acciones
 *   npx playwright test --ui             → interfaz gráfica interactiva
 */
export default defineConfig({
  /* Directorio donde viven los tests E2E */
  testDir: './tests',

  /* Tiempo máximo por test completo (30 s es suficiente con mocks) */
  timeout: 30_000,

  /* Tiempo máximo de espera para cada aserción expect() */
  expect: { timeout: 5_000 },

  /* E2E de flujo secuencial → no paralelizar */
  fullyParallel: false,

  /* Sin reintentos automáticos en desarrollo */
  retries: 0,

  /* Reporter legible en terminal */
  reporter: 'list',

  use: {
    /* URL base del servidor de desarrollo Vite */
    baseURL: 'http://localhost:5173',

    /* headless: true por defecto. El flag --headed lo sobreescribe en runtime. */
    headless: true,

    viewport: { width: 1280, height: 720 },

    /* Captura screenshot solo cuando un test falla */
    screenshot: 'only-on-failure',

    /* Para ver las acciones a cámara lenta en modo --headed,
       descomenta y ajusta el valor en milisegundos: */
    // launchOptions: { slowMo: 400 },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  /* Opcional: arranca el servidor Vite automáticamente antes de los tests.
     Descomenta si quieres que Playwright gestione el arranque: */
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: true,
  //   timeout: 30_000,
  // },
})
