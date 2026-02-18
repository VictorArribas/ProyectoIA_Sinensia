/**
 * Navbar Component - Navigation with logout
 */
import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link to="/" style={styles.logo}>
          💪 Smart AI Gym Coach
        </Link>

        <div style={styles.links}>
          {user ? (
            <>
              <Link to="/profile" style={styles.link}>
                Perfil
              </Link>
              <Link to="/workouts" style={styles.link}>
                Entrenamientos
              </Link>
              <span style={styles.email}>{user.email}</span>
              <button onClick={handleLogout} style={styles.logoutButton}>
                Cerrar Sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>
                Iniciar Sesión
              </Link>
              <Link to="/register" style={styles.link}>
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '15px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: 'white',
    textDecoration: 'none',
  },
  links: {
    display: 'flex',
    gap: '20px',
    alignItems: 'center',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '16px',
    transition: 'opacity 0.2s',
  },
  email: {
    color: 'white',
    fontSize: '14px',
    opacity: 0.8,
  },
  logoutButton: {
    padding: '8px 16px',
    background: 'rgba(255, 255, 255, 0.2)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
}

export default Navbar
