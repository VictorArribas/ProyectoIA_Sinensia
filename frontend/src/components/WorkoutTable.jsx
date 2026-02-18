/**
 * WorkoutTable Component - Display workout plan exercises
 */
import React from 'react'

const WorkoutTable = ({ workoutPlan, disclaimer }) => {
  if (!workoutPlan || workoutPlan.length === 0) {
    return <p>No hay ejercicios en este plan.</p>
  }

  return (
    <div style={styles.container}>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Músculo</th>
            <th style={styles.th}>Ejercicio</th>
            <th style={styles.th}>Series</th>
            <th style={styles.th}>Repeticiones</th>
            <th style={styles.th}>RPE</th>
            <th style={styles.th}>Descanso</th>
            <th style={styles.th}>Notas de Seguridad</th>
          </tr>
        </thead>
        <tbody>
          {workoutPlan.map((exercise, index) => (
            <tr key={index} style={index % 2 === 0 ? styles.evenRow : styles.oddRow}>
              <td style={styles.td}>{exercise.musculo}</td>
              <td style={styles.td}>
                <strong>{exercise.ejercicio}</strong>
              </td>
              <td style={styles.td}>{exercise.series}</td>
              <td style={styles.td}>{exercise.repeticiones}</td>
              <td style={styles.td}>{exercise.rpe_objetivo}/10</td>
              <td style={styles.td}>{Math.floor(exercise.descanso_segundos / 60)}:{String(exercise.descanso_segundos % 60).padStart(2, '0')}</td>
              <td style={styles.td}>
                <small>{exercise.notas_seguridad}</small>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {disclaimer && (
        <div style={styles.disclaimer}>
          <strong>⚠️ Disclaimer Médico:</strong> {disclaimer}
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    marginTop: '20px',
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  th: {
    padding: '12px',
    textAlign: 'left',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontWeight: 'bold',
    borderBottom: '2px solid #ddd',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #ddd',
  },
  evenRow: {
    backgroundColor: '#f9f9f9',
  },
  oddRow: {
    backgroundColor: 'white',
  },
  disclaimer: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    fontSize: '14px',
  },
}

export default WorkoutTable
