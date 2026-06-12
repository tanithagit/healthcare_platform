import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import {
  getMyAppointments,
  cancelAppointment
} from '../../api/appointmentApi'

const MyAppointments = () => {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchAppointments()
  }, [])

  const fetchAppointments = async () => {
    try {
      const data = await getMyAppointments()
      setAppointments(data)
    } catch (err) {
      setError('Failed to load appointments')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('Cancel this appointment?')) return
    try {
      await cancelAppointment(id)
      setSuccess('Appointment cancelled successfully')
      fetchAppointments()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to cancel appointment'
      )
    }
  }

  const getStatusColor = (status) => {
    if (status === 'scheduled') return 'bg-blue-100 text-blue-700'
    if (status === 'completed') return 'bg-green-100 text-green-700'
    return 'bg-red-100 text-red-700'
  }

  const filtered = filter === 'all'
    ? appointments
    : appointments.filter(a => a.status === filter)

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            My Appointments
          </h1>
          <p className="text-gray-500 mt-1">
            Track all your appointments
          </p>
        </div>

        {/* Messages */}
        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            ❌ {error}
          </div>
        )}
        {success && (
          <div className="bg-green-50 border border-green-200
                          text-green-600 rounded-lg p-4">
            ✅ {success}
          </div>
        )}

        {/* Filter Tabs */}
        <div className="flex gap-2">
          {['all', 'scheduled', 'completed', 'canceled'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium
                          capitalize transition
                ${filter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
                }`}
            >
              {f}
            </button>
          ))}
        </div>

        {/* Appointments */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10
                            border-b-2 border-blue-600"></div>
          </div>
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center
                          text-gray-400">
            <p className="text-4xl mb-2">📅</p>
            <p>No appointments found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map((apt) => (
              <div key={apt.id}
                className="bg-white rounded-xl shadow-sm border
                           border-gray-100 p-6">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-semibold text-gray-800">
                        Dr. {apt.doctor_email?.split('@')[0]}
                      </h3>
                      <span className={`px-2 py-0.5 rounded-full
                                       text-xs font-medium
                                       ${getStatusColor(apt.status)}`}>
                        {apt.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500">
                      📅 {new Date(apt.appointment_date)
                        .toLocaleString()}
                    </p>
                    {apt.reason && (
                      <p className="text-sm text-gray-600">
                        📋 {apt.reason}
                      </p>
                    )}
                    <p className="text-sm font-medium text-gray-700">
                      💰 Fee: ₹{apt.consultation_fee}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    {apt.status === 'scheduled' && (
                      <button
                        onClick={() => handleCancel(apt.id)}
                        className="bg-red-50 text-red-600 px-3 py-1.5
                                   rounded-lg text-sm hover:bg-red-100"
                      >
                        Cancel
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}

export default MyAppointments