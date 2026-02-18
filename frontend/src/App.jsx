/**
 * App - Main application with routing
 */
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import WorkoutsPage from './pages/WorkoutsPage'

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Cargando...</div>
  }

  return user ? children : <Navigate to="/login" />
}

// Home page
const HomePage = () => {
  const { user } = useAuth()

  if (user) {
    return <Navigate to="/workouts" />
  }

  return (
    <div
      style={{
        minHeight: 'calc(100vh - 60px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>💪 Smart AI Gym Coach</h1>
        <p style={{ fontSize: '1.5rem', opacity: 0.9, marginBottom: '2rem' }}>
          Coach deportivo inteligente con LLM
        </p>
        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
          <a
            href="/register"
            style={{
              padding: '12px 24px',
              background: 'white',
              color: '#667eea',
              textDecoration: 'none',
              borderRadius: '4px',
              fontWeight: 'bold',
            }}
          >
            Registrarse
          </a>
          <a
            href="/login"
            style={{
              padding: '12px 24px',
              background: 'rgba(255,255,255,0.2)',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '4px',
              fontWeight: 'bold',
              border: '1px solid white',
            }}
          >
            Iniciar Sesión
          </a>
        </div>
      </div>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <div style={{ minHeight: '100vh', background: '#f5f5f5' }}>
          <Navbar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/workouts"
              element={
                <ProtectedRoute>
                  <WorkoutsPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
