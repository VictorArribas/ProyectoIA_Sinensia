/**
 * Workout Service - API calls for workout generation and history
 */
import api from './api'

const workoutService = {
  /**
   * Generate new workout plan
   * @param {number} fatigueScore - Optional fatigue score (0-100, defaults to 50)
   * @returns {Promise} Generated workout plan
   */
  generateWorkout: async (fatigueScore = 50) => {
    const response = await api.post('/workouts/generate', {
      fatigue_score: fatigueScore,
    })
    return response.data
  },

  /**
   * Get workout history (last 30 plans)
   * @returns {Promise} Array of workout history items
   */
  getHistory: async () => {
    const response = await api.get('/workouts/history')
    return response.data
  },

  /**
   * Get specific workout plan by ID
   * @param {number} workoutPlanId - Workout plan ID
   * @returns {Promise} Full workout plan details
   */
  getWorkoutById: async (workoutPlanId) => {
    const response = await api.get(`/workouts/${workoutPlanId}`)
    return response.data
  },
}

export default workoutService
