export const getRoleDashboard = (role) => {
  if (role === 'admin') return '/admin/dashboard'
  if (role === 'doctor') return '/doctor/dashboard'
  if (role === 'patient') return '/patient/dashboard'
  return '/login'
}