/**
 * Profile Service - API calls for user profile
 */
import api from './api'

const profileService = {
  /**
   * Get current user's profile
   * @returns {Promise} User profile data
   */
  getProfile: async () => {
    const response = await api.get('/profile/me')
    return response.data
  },

  /**
   * Create user profile (onboarding)
   * @param {Object} profileData - Profile data
   * @returns {Promise} Created profile
   */
  createProfile: async (profileData) => {
    const response = await api.post('/profile/create', profileData)
    return response.data
  },

  /**
   * Update user profile
   * @param {Object} updates - Fields to update (partial)
   * @returns {Promise} Updated profile
   */
  updateProfile: async (updates) => {
    const response = await api.put('/profile/update', updates)
    return response.data
  },
}

export default profileService
