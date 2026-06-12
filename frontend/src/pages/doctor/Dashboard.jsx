import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import { useAuth } from '../../context/AuthContext'
import { getDoctorAppointments } from '../../api/appointmentApi'

const DoctorDashboard = () => {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAppointments()
  }, [])

  const fetchAppointments = async () => {
    try {
      const data = await getDoctorAppointments()
      setAppointments(data)
    } catch (err) {
      setError('Failed to load appointments')
    } finally {
      setLoading(false)
    }
  }

  // Filter today's appointments
  const today = new Date().toDateString()
  const todayAppointments = appointments.filter(apt => {
    const aptDate = new Date(apt.appointment_date).toDateString()
    return aptDate === today
  })

  const scheduled = appointments.filter(a => a.status === 'scheduled')
  const completed = appointments.filter(a => a.status === 'completed')

  const getStatusColor = (status) => {
    if (status === 'scheduled') return 'bg-blue-100 text-blue-700'
    if (status === 'completed') return 'bg-green-100 text-green-700'
    return 'bg-red-100 text-red-700'
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Doctor Dashboard
          </h1>
          <p className="text-gray-500 mt-1">
            Welcome back, Dr. {user?.email?.split('@')[0]}!
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            {error}
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Today's Appointments</p>
            <p className="text-3xl font-bold text-blue-600 mt-1">
              {todayAppointments.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">📅 Today</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Scheduled</p>
            <p className="text-3xl font-bold text-yellow-600 mt-1">
              {scheduled.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">⏳ Pending</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Completed</p>
            <p className="text-3xl font-bold text-green-600 mt-1">
              {completed.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">✅ Done</p>
          </div>
        </div>

        {/* Today's Appointments */}
        <div className="bg-white rounded-xl shadow-sm border
                        border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            📅 Today's Appointments
          </h2>

          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8
                              border-b-2 border-blue-600"></div>
            </div>
          ) : todayAppointments.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <p className="text-3xl mb-2">📅</p>
              <p>No appointments today</p>
            </div>
          ) : (
            <div className="space-y-3">
              {todayAppointments.map((apt) => (
                <div key={apt.id}
                  className="flex items-center justify-between
                             p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">
                      Patient: {apt.patient_email}
                    </p>
                    <p className="text-sm text-gray-500 mt-0.5">
                      🕐 {new Date(apt.appointment_date)
                        .toLocaleTimeString()}
                      {apt.reason && ` • ${apt.reason}`}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs
                                   font-medium ${getStatusColor(apt.status)}`}>
                    {apt.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent All Appointments */}
        <div className="bg-white rounded-xl shadow-sm border
                        border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            📋 All Appointments
          </h2>
          {appointments.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <p>No appointments yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {appointments.slice(0, 5).map((apt) => (
                <div key={apt.id}
                  className="flex items-center justify-between
                             p-4 border border-gray-100 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">
                      {apt.patient_email}
                    </p>
                    <p className="text-sm text-gray-500">
                      {new Date(apt.appointment_date)
                        .toLocaleDateString()}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs
                                   font-medium ${getStatusColor(apt.status)}`}>
                    {apt.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </Layout>
  )
}

export default DoctorDashboard