import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import { useAuth } from '../../context/AuthContext'
import { getMyAppointments } from '../../api/appointmentApi'
import { getMyInvoices } from '../../api/billingApi'
import { Link } from 'react-router-dom'

const PatientDashboard = () => {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState([])
  const [invoices, setInvoices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [aptsData, invoicesData] = await Promise.all([
        getMyAppointments(),
        getMyInvoices()
      ])
      setAppointments(aptsData)
      setInvoices(invoicesData)
    } catch (err) {
      console.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const upcoming = appointments.filter(
    a => a.status === 'scheduled'
  )
  const completed = appointments.filter(
    a => a.status === 'completed'
  )
  const pendingPayments = invoices.filter(
    i => i.payment_status === 'pending'
  )

  const getStatusColor = (status) => {
    if (status === 'scheduled') return 'bg-blue-100 text-blue-700'
    if (status === 'completed') return 'bg-green-100 text-green-700'
    return 'bg-red-100 text-red-700'
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">
              Patient Dashboard
            </h1>
            <p className="text-gray-500 mt-1">
              Welcome, {user?.email?.split('@')[0]}!
            </p>
          </div>
          <Link to="/patient/book"
            className="bg-blue-600 text-white px-5 py-2.5
                       rounded-lg font-medium hover:bg-blue-700
                       transition flex items-center gap-2">
            + Book Appointment
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Upcoming</p>
            <p className="text-3xl font-bold text-blue-600 mt-1">
              {upcoming.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">
              📅 Appointments
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Completed</p>
            <p className="text-3xl font-bold text-green-600 mt-1">
              {completed.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">
              ✅ Consultations
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Pending Payments</p>
            <p className="text-3xl font-bold text-red-600 mt-1">
              {pendingPayments.length}
            </p>
            <p className="text-xs text-gray-400 mt-1">
              💳 Invoices
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { to: '/patient/book', icon: '📅',
              label: 'Book Appointment', color: 'bg-blue-50' },
            { to: '/patient/appointments', icon: '🗓️',
              label: 'My Appointments', color: 'bg-green-50' },
            { to: '/patient/history', icon: '📋',
              label: 'Medical History', color: 'bg-purple-50' },
            { to: '/patient/billing', icon: '💳',
              label: 'Billing', color: 'bg-yellow-50' },
          ].map((action) => (
            <Link key={action.to} to={action.to}
              className={`${action.color} rounded-xl p-5 text-center
                          hover:shadow-md transition`}>
              <p className="text-3xl mb-2">{action.icon}</p>
              <p className="text-sm font-medium text-gray-700">
                {action.label}
              </p>
            </Link>
          ))}
        </div>

        {/* Upcoming Appointments */}
        <div className="bg-white rounded-xl shadow-sm border
                        border-gray-100 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">
              📅 Upcoming Appointments
            </h2>
            <Link to="/patient/appointments"
              className="text-sm text-blue-600 hover:underline">
              View all →
            </Link>
          </div>

          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8
                              border-b-2 border-blue-600"></div>
            </div>
          ) : upcoming.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <p className="text-3xl mb-2">📅</p>
              <p>No upcoming appointments</p>
              <Link to="/patient/book"
                className="mt-3 inline-block text-blue-600
                           hover:underline text-sm">
                Book your first appointment →
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {upcoming.map((apt) => (
                <div key={apt.id}
                  className="flex items-center justify-between
                             p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">
                      Dr. {apt.doctor_email?.split('@')[0]}
                    </p>
                    <p className="text-sm text-gray-500">
                      📅 {new Date(apt.appointment_date)
                        .toLocaleString()}
                    </p>
                    {apt.reason && (
                      <p className="text-xs text-gray-400 mt-0.5">
                        {apt.reason}
                      </p>
                    )}
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs
                                   font-medium
                                   ${getStatusColor(apt.status)}`}>
                    {apt.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pending Payments */}
        {pendingPayments.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200
                          rounded-xl p-6">
            <h2 className="text-lg font-semibold text-yellow-800 mb-4">
              ⚠️ Pending Payments
            </h2>
            <div className="space-y-3">
              {pendingPayments.map((invoice) => (
                <div key={invoice.id}
                  className="flex items-center justify-between
                             bg-white p-4 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">
                      Invoice #{invoice.id}
                    </p>
                    <p className="text-sm text-gray-500">
                      Appointment #{invoice.appointment_id}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-gray-800">
                      ₹{invoice.amount}
                    </span>
                    <Link to="/patient/billing"
                      className="bg-yellow-500 text-white px-4 py-1.5
                                 rounded-lg text-sm hover:bg-yellow-600">
                      Pay Now
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </Layout>
  )
}

export default PatientDashboard