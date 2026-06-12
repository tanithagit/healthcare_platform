import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import axios from '../../api/axios'

const ManagePatients = () => {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchPatients()
  }, [])

  const fetchPatients = async () => {
    try {
      const response = await axios.get('/api/patients/')
      setPatients(response.data)
    } catch (err) {
      setError('Failed to load patients')
    } finally {
      setLoading(false)
    }
  }

  const handleDeactivate = async (userId) => {
    if (!window.confirm('Deactivate this patient?')) return
    try {
      await axios.put(`/api/admin/users/${userId}/deactivate`)
      fetchPatients()
    } catch (err) {
      setError('Failed to deactivate patient')
    }
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Manage Patients
          </h1>
          <p className="text-gray-500 mt-1">
            View and manage all registered patients
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10
                            border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm
                          border border-gray-100 overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Patient</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Phone</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Blood Group</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {patients.map((patient) => (
                  <tr key={patient.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-green-100
                                        flex items-center justify-center
                                        text-green-600 font-semibold">
                          {patient.email?.charAt(0).toUpperCase()}
                        </div>
                        <p className="text-sm font-medium text-gray-800">
                          {patient.email}
                        </p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {patient.phone || 'Not provided'}
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-red-50 text-red-700
                                       rounded-full text-xs font-medium">
                        {patient.blood_group || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleDeactivate(patient.user_id)}
                        className="bg-red-50 text-red-600 px-3 py-1
                                   rounded text-sm hover:bg-red-100"
                      >
                        Deactivate
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {patients.length === 0 && (
              <div className="text-center py-12 text-gray-400">
                <p className="text-4xl mb-2">👤</p>
                <p>No patients registered yet</p>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  )
}

export default ManagePatients