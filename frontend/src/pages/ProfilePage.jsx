/**
 * ProfilePage - Create/update user profile
 */
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ProfileForm from '../components/ProfileForm'
import profileService from '../services/profileService'

const ProfilePage = () => {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      const data = await profileService.getProfile()
      setProfile(data)
    } catch (err) {
      // Profile not found - user needs to create one
      if (err.response?.status === 404) {
        setProfile(null)
      } else {
        setError('Error al cargar perfil')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (formData) => {
    try {
      if (profile) {
        await profileService.updateProfile(formData)
        alert('Perfil actualizado correctamente')
      } else {
        await profileService.createProfile(formData)
        alert('Perfil creado correctamente. Ahora puedes generar tu plan de entrenamiento.')
        navigate('/workouts')
      }
      await loadProfile()
    } catch (err) {
      throw err
    }
  }

  if (loading) {
    return (
      <div style={styles.container}>
        <p>Cargando perfil...</p>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>
        {profile ? 'Actualizar Perfil' : 'Crear Perfil'}
      </h1>

      {error && <div style={styles.error}>{error}</div>}

      {!profile && (
        <p style={styles.subtitle}>
          Completa tu perfil para recibir planes de entrenamiento personalizados.
        </p>
      )}

      <ProfileForm
        initialData={profile}
        onSubmit={handleSubmit}
        onCancel={profile ? () => navigate('/workouts') : null}
      />
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '800px',
    margin: '40px auto',
    padding: '20px',
  },
  title: {
    fontSize: '32px',
    marginBottom: '10px',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    textAlign: 'center',
    marginBottom: '30px',
  },
  error: {
    padding: '12px',
    marginBottom: '20px',
    background: '#fee',
    color: '#c33',
    borderRadius: '4px',
    border: '1px solid #fcc',
  },
}

export default ProfilePage
