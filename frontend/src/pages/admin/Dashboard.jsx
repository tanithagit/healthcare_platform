import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import axios from '../../api/axios'

const StatCard = ({ title, value, icon, color }) => (
  <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500 font-medium">{title}</p>
        <p className={`text-3xl font-bold mt-1 ${color}`}>{value}</p>
      </div>
      <div className="text-4xl">{icon}</div>
    </div>
  </div>
)

const AdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/admin/dashboard')
      setStats(response.data)
    } catch (err) {
      setError('Failed to load dashboard stats')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12
                          border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Admin Dashboard
          </h1>
          <p className="text-gray-500 mt-1">
            Welcome back! Here's your platform overview.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            {error}
          </div>
        )}

        {/* Stats Grid */}
        {stats && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2
                            lg:grid-cols-4 gap-6">
              <StatCard
                title="Total Doctors"
                value={stats.total_doctors}
                icon="👨‍⚕️"
                color="text-blue-600"
              />
              <StatCard
                title="Total Patients"
                value={stats.total_patients}
                icon="👤"
                color="text-green-600"
              />
              <StatCard
                title="Total Appointments"
                value={stats.total_appointments}
                icon="📅"
                color="text-purple-600"
              />
              <StatCard
                title="Total Revenue"
                value={`₹${stats.total_revenue}`}
                icon="💰"
                color="text-yellow-600"
              />
            </div>

            {/* Appointment Stats */}
            <div className="bg-white rounded-xl shadow-sm p-6
                            border border-gray-100">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">
                📊 Appointment Overview
              </h2>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50
                                rounded-lg">
                  <p className="text-2xl font-bold text-blue-600">
                    {stats.appointments.scheduled}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">Scheduled</p>
                </div>
                <div className="text-center p-4 bg-green-50
                                rounded-lg">
                  <p className="text-2xl font-bold text-green-600">
                    {stats.appointments.completed}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">Completed</p>
                </div>
                <div className="text-center p-4 bg-red-50
                                rounded-lg">
                  <p className="text-2xl font-bold text-red-600">
                    {stats.appointments.canceled}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">Canceled</p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </Layout>
  )
}

export default AdminDashboard