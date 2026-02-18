/**
 * ProfileForm Component - User profile creation/update form
 */
import React, { useState } from 'react'

const ProfileForm = ({ initialData = null, onSubmit, onCancel = null }) => {
  const [formData, setFormData] = useState({
    age: initialData?.age || '',
    weight_kg: initialData?.weight_kg || '',
    height_cm: initialData?.height_cm || '',
    objective: initialData?.objective || 'hypertrophy',
    experience_level: initialData?.experience_level || 'beginner',
    training_days_per_week: initialData?.training_days_per_week || 3,
    equipment_available: initialData?.equipment_available || ['dumbbells', 'barbell', 'bodyweight'],
    injury_history: initialData?.injury_history || [],
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target

    if (type === 'checkbox') {
      // Handle equipment checkboxes
      const currentEquipment = [...formData.equipment_available]
      if (checked) {
        currentEquipment.push(value)
      } else {
        const index = currentEquipment.indexOf(value)
        if (index > -1) currentEquipment.splice(index, 1)
      }
      setFormData({ ...formData, equipment_available: currentEquipment })
    } else {
      setFormData({ ...formData, [name]: value })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Convert numeric fields
      const submitData = {
        ...formData,
        age: parseInt(formData.age),
        weight_kg: parseFloat(formData.weight_kg),
        height_cm: parseFloat(formData.height_cm),
        training_days_per_week: parseInt(formData.training_days_per_week),
      }

      await onSubmit(submitData)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al guardar perfil')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.row}>
        <div style={styles.field}>
          <label>Edad *</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            min="13"
            max="120"
            required
            style={styles.input}
          />
        </div>

        <div style={styles.field}>
          <label>Peso (kg) *</label>
          <input
            type="number"
            name="weight_kg"
            value={formData.weight_kg}
            onChange={handleChange}
            min="1"
            step="0.1"
            required
            style={styles.input}
          />
        </div>

        <div style={styles.field}>
          <label>Altura (cm) *</label>
          <input
            type="number"
            name="height_cm"
            value={formData.height_cm}
            onChange={handleChange}
            min="1"
            step="0.1"
            required
            style={styles.input}
          />
        </div>
      </div>

      <div style={styles.field}>
        <label>Objetivo *</label>
        <select
          name="objective"
          value={formData.objective}
          onChange={handleChange}
          required
          style={styles.input}
        >
          <option value="hypertrophy">Hipertrofia (ganancia muscular)</option>
          <option value="cutting">Definición (pérdida de grasa)</option>
          <option value="strength">Fuerza máxima</option>
          <option value="recomposition">Recomposición corporal</option>
        </select>
      </div>

      <div style={styles.field}>
        <label>Nivel de experiencia *</label>
        <select
          name="experience_level"
          value={formData.experience_level}
          onChange={handleChange}
          required
          style={styles.input}
        >
          <option value="beginner">Principiante</option>
          <option value="intermediate">Intermedio</option>
          <option value="advanced">Avanzado</option>
        </select>
      </div>

      <div style={styles.field}>
        <label>Días de entrenamiento por semana *</label>
        <input
          type="number"
          name="training_days_per_week"
          value={formData.training_days_per_week}
          onChange={handleChange}
          min="1"
          max="7"
          required
          style={styles.input}
        />
      </div>

      <div style={styles.field}>
        <label>Equipamiento disponible * (selecciona al menos 1)</label>
        <div style={styles.checkboxGroup}>
          {['dumbbells', 'barbell', 'cables', 'machines', 'bodyweight'].map((equipment) => (
            <label key={equipment} style={styles.checkbox}>
              <input
                type="checkbox"
                value={equipment}
                checked={formData.equipment_available.includes(equipment)}
                onChange={handleChange}
              />
              <span style={{ marginLeft: '8px' }}>
                {equipment === 'dumbbells' && 'Mancuernas'}
                {equipment === 'barbell' && 'Barra'}
                {equipment === 'cables' && 'Cables/Poleas'}
                {equipment === 'machines' && 'Máquinas'}
                {equipment === 'bodyweight' && 'Peso corporal'}
              </span>
            </label>
          ))}
        </div>
      </div>

      <div style={styles.buttons}>
        <button type="submit" disabled={loading} style={styles.submitButton}>
          {loading ? 'Guardando...' : initialData ? 'Actualizar Perfil' : 'Crear Perfil'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} style={styles.cancelButton}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}

const styles = {
  form: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
  },
  row: {
    display: 'flex',
    gap: '15px',
    marginBottom: '15px',
  },
  field: {
    marginBottom: '15px',
    flex: 1,
  },
  input: {
    width: '100%',
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    boxSizing: 'border-box',
  },
  checkboxGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    marginTop: '8px',
  },
  checkbox: {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
  },
  buttons: {
    display: 'flex',
    gap: '10px',
    marginTop: '20px',
  },
  submitButton: {
    padding: '12px 24px',
    fontSize: '16px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    flex: 1,
  },
  cancelButton: {
    padding: '12px 24px',
    fontSize: '16px',
    background: '#ccc',
    color: '#333',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  error: {
    padding: '12px',
    marginBottom: '15px',
    background: '#fee',
    color: '#c33',
    borderRadius: '4px',
    border: '1px solid #fcc',
  },
}

export default ProfileForm
