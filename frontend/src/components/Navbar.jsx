import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const getRoleColor = (role) => {
    if (role === 'admin') return 'bg-purple-100 text-purple-700'
    if (role === 'doctor') return 'bg-green-100 text-green-700'
    return 'bg-blue-100 text-blue-700'
  }

  const getRoleIcon = (role) => {
    if (role === 'admin') return '👑'
    if (role === 'doctor') return '👨‍⚕️'
    return '👤'
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-2">
          <span className="text-2xl">🏥</span>
          <span className="font-bold text-gray-800 text-lg">
            Healthcare Platform
          </span>
        </div>

        {/* User Info */}
        {user && (
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-full text-xs font-medium
                              ${getRoleColor(user.role)}`}>
                {getRoleIcon(user.role)} {user.role.toUpperCase()}
              </span>
              <span className="text-sm text-gray-600">{user.email}</span>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-50 text-red-600 px-4 py-2 rounded-lg
                         text-sm font-medium hover:bg-red-100 transition"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar