/**
 * WorkoutsPage - Generate workout plans and view history
 */
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import WorkoutTable from '../components/WorkoutTable'
import workoutService from '../services/workoutService'
import profileService from '../services/profileService'

const WorkoutsPage = () => {
  const [currentWorkout, setCurrentWorkout] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [hasProfile, setHasProfile] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    checkProfile()
    loadHistory()
  }, [])

  const checkProfile = async () => {
    try {
      await profileService.getProfile()
      setHasProfile(true)
    } catch (err) {
      if (err.response?.status === 404) {
        setHasProfile(false)
      }
    }
  }

  const loadHistory = async () => {
    try {
      const data = await workoutService.getHistory()
      setHistory(data)
    } catch (err) {
      console.error('Error loading history:', err)
    }
  }

  const handleGenerateWorkout = async () => {
    if (!hasProfile) {
      alert('Por favor, crea tu perfil primero')
      navigate('/profile')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const workout = await workoutService.generateWorkout(50)
      setCurrentWorkout(workout)
      await loadHistory() // Refresh history
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al generar plan de entrenamiento')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Planes de Entrenamiento</h1>

      {!hasProfile && (
        <div style={styles.warning}>
          ⚠️ Necesitas crear tu perfil primero.{' '}
          <a href="/profile" style={{ color: '#667eea', fontWeight: 'bold' }}>
            Ir a Perfil
          </a>
        </div>
      )}

      <div style={styles.actions}>
        <button
          onClick={handleGenerateWorkout}
          disabled={loading || !hasProfile}
          style={styles.generateButton}
        >
          {loading ? '⏳ Generando con Claude AI...' : '🤖 Generar Plan de Entrenamiento'}
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      {currentWorkout && (
        <div style={styles.workoutSection}>
          <h2 style={styles.subtitle}>Tu Plan de Entrenamiento</h2>
          <p style={styles.info}>
            Score de fatiga usado: <strong>{currentWorkout.fatiga_score_usado}/100</strong>
            {currentWorkout.ajuste_aplicado && (
              <span style={{ marginLeft: '20px', color: '#666' }}>
                Ajuste: {currentWorkout.ajuste_aplicado}
              </span>
            )}
          </p>
          <WorkoutTable
            workoutPlan={currentWorkout.workout_plan}
            disclaimer={currentWorkout.disclaimer_medico}
          />
        </div>
      )}

      {history.length > 0 && (
        <div style={styles.historySection}>
          <h2 style={styles.subtitle}>Historial de Entrenamientos</h2>
          <table style={styles.historyTable}>
            <thead>
              <tr>
                <th style={styles.th}>Fecha</th>
                <th style={styles.th}>Ejercicios</th>
                <th style={styles.th}>Fatiga</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id} style={styles.historyRow}>
                  <td style={styles.td}>{new Date(item.created_at).toLocaleDateString('es-ES')}</td>
                  <td style={styles.td}>{item.exercise_count} ejercicios</td>
                  <td style={styles.td}>{item.fatigue_score_used}/100</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '40px auto',
    padding: '20px',
  },
  title: {
    fontSize: '32px',
    marginBottom: '20px',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: '24px',
    marginBottom: '15px',
  },
  info: {
    fontSize: '16px',
    color: '#666',
    marginBottom: '20px',
  },
  actions: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  generateButton: {
    padding: '15px 30px',
    fontSize: '18px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  warning: {
    padding: '15px',
    marginBottom: '20px',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    textAlign: 'center',
  },
  error: {
    padding: '15px',
    marginBottom: '20px',
    background: '#fee',
    color: '#c33',
    borderRadius: '4px',
    border: '1px solid #fcc',
  },
  workoutSection: {
    marginBottom: '40px',
  },
  historySection: {
    marginTop: '40px',
  },
  historyTable: {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  th: {
    padding: '12px',
    textAlign: 'left',
    background: '#f5f5f5',
    fontWeight: 'bold',
    borderBottom: '2px solid #ddd',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #ddd',
  },
  historyRow: {
    cursor: 'pointer',
    transition: 'background 0.2s',
  },
}

export default WorkoutsPage
