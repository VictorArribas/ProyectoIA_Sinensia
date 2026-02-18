/**
 * Authentication Service - API calls for auth operations
 */
import api from './api'

const authService = {
  /**
   * Register a new user
   * @param {string} email - User email
   * @param {string} password - User password (min 8 chars)
   * @returns {Promise} Response with access_token, refresh_token
   */
  register: async (email, password) => {
    const response = await api.post('/auth/register', { email, password })
    return response.data
  },

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} Response with access_token, refresh_token
   */
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  /**
   * Refresh access token
   * @param {string} refreshToken - JWT refresh token
   * @returns {Promise} Response with new access_token
   */
  refresh: async (refreshToken) => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },

  /**
   * Store tokens in localStorage
   * @param {string} accessToken - JWT access token
   * @param {string} refreshToken - JWT refresh token
   * @param {string} email - User email
   */
  storeTokens: (accessToken, refreshToken, email) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    localStorage.setItem('user_email', email)
  },

  /**
   * Clear tokens from localStorage
   */
  clearTokens: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_email')
  },

  /**
   * Get current user email from localStorage
   * @returns {string|null} User email or null if not logged in
   */
  getCurrentUserEmail: () => {
    return localStorage.getItem('user_email')
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} True if access token exists
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token')
  },
}

export default authService
