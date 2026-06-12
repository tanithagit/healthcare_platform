import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Sidebar = () => {
  const { user } = useAuth()

  const adminLinks = [
    { path: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/admin/doctors', label: 'Manage Doctors', icon: '👨‍⚕️' },
    { path: '/admin/patients', label: 'Manage Patients', icon: '👤' },
  ]

  const doctorLinks = [
    { path: '/doctor/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/doctor/appointments', label: 'Appointments', icon: '📅' },
    { path: '/doctor/prescriptions', label: 'Prescriptions', icon: '💊' },
  ]

  const patientLinks = [
    { path: '/patient/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/patient/book', label: 'Book Appointment', icon: '📅' },
    { path: '/patient/appointments', label: 'My Appointments', icon: '🗓️' },
    { path: '/patient/history', label: 'Medical History', icon: '📋' },
    { path: '/patient/billing', label: 'Billing', icon: '💳' },
  ]

  const getLinks = () => {
    if (user?.role === 'admin') return adminLinks
    if (user?.role === 'doctor') return doctorLinks
    return patientLinks
  }

  return (
    <aside className="w-64 min-h-screen bg-gray-900 text-white
                      flex flex-col">

      {/* Role Header */}
      <div className="p-6 border-b border-gray-700">
        <p className="text-xs text-gray-400 uppercase tracking-wider">
          {user?.role} Portal
        </p>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-4 space-y-1">
        {getLinks().map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg
               transition text-sm font-medium
               ${isActive
                 ? 'bg-blue-600 text-white'
                 : 'text-gray-300 hover:bg-gray-800 hover:text-white'
               }`
            }
          >
            <span>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Bottom User Info */}
      <div className="p-4 border-t border-gray-700">
        <p className="text-xs text-gray-400 truncate">{user?.email}</p>
      </div>
    </aside>
  )
}

export default Sidebar