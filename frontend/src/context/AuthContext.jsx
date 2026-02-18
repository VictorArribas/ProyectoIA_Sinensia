/**
 * AuthContext - Global authentication state management
 * Provides login, logout, register, and user state
 */
import React, { createContext, useState, useContext, useEffect } from 'react'
import authService from '../services/authService'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initAuth = () => {
      const email = authService.getCurrentUserEmail()
      if (email && authService.isAuthenticated()) {
        setUser({ email })
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  /**
   * Register new user
   * @param {string} email - User email
   * @param {string} password - User password (min 8 chars)
   * @returns {Promise} Resolves on success, rejects on error
   */
  const register = async (email, password) => {
    try {
      const data = await authService.register(email, password)
      authService.storeTokens(data.access_token, data.refresh_token, email)
      setUser({ email })
      return data
    } catch (error) {
      throw error
    }
  }

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} Resolves on success, rejects on error
   */
  const login = async (email, password) => {
    try {
      const data = await authService.login(email, password)
      authService.storeTokens(data.access_token, data.refresh_token, email)
      setUser({ email })
      return data
    } catch (error) {
      throw error
    }
  }

  /**
   * Logout user - clear tokens and reset state
   */
  const logout = () => {
    authService.clearTokens()
    setUser(null)
  }

  const value = {
    user,
    loading,
    register,
    login,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

/**
 * Hook to access auth context
 * @returns {Object} Auth context with user, login, logout, register, isAuthenticated
 */
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export default AuthContext
