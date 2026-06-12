import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import axios from '../../api/axios'

const ManageDoctors = () => {
  const [doctors, setDoctors] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [editDoctor, setEditDoctor] = useState(null)
  const [editForm, setEditForm] = useState({})

  useEffect(() => {
    fetchDoctors()
  }, [])

  const fetchDoctors = async () => {
    try {
      const response = await axios.get('/api/doctors/')
      setDoctors(response.data)
    } catch (err) {
      setError('Failed to load doctors')
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (doctor) => {
    setEditDoctor(doctor.id)
    setEditForm({
      specialization: doctor.specialization,
      experience_years: doctor.experience_years,
      consultation_fee: doctor.consultation_fee,
      qualification: doctor.qualification || '',
      bio: doctor.bio || '',
    })
  }

  const handleUpdate = async (doctorId) => {
    try {
      await axios.put(`/api/doctors/${doctorId}`, editForm)
      setSuccess('Doctor updated successfully!')
      setEditDoctor(null)
      fetchDoctors()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Failed to update doctor')
    }
  }

  const handleDeactivate = async (doctorId) => {
    if (!window.confirm('Are you sure you want to deactivate this doctor?'))
      return
    try {
      await axios.delete(`/api/doctors/${doctorId}`)
      setSuccess('Doctor deactivated successfully!')
      fetchDoctors()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Failed to deactivate doctor')
    }
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Manage Doctors
          </h1>
          <p className="text-gray-500 mt-1">
            View and manage all registered doctors
          </p>
        </div>

        {/* Messages */}
        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-50 border border-green-200
                          text-green-600 rounded-lg p-4">
            ✅ {success}
          </div>
        )}

        {/* Doctors Table */}
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
                                  text-gray-500 uppercase">Doctor</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Specialization</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Experience</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Fee</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold
                                  text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {doctors.map((doctor) => (
                  <tr key={doctor.id} className="hover:bg-gray-50">
                    {editDoctor === doctor.id ? (
                      <>
                        <td className="px-6 py-4">
                          <p className="text-sm font-medium text-gray-800">
                            {doctor.email}
                          </p>
                        </td>
                        <td className="px-6 py-4">
                          <input
                            value={editForm.specialization}
                            onChange={(e) => setEditForm({
                              ...editForm,
                              specialization: e.target.value
                            })}
                            className="border rounded px-2 py-1 text-sm
                                       w-full"
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            type="number"
                            value={editForm.experience_years}
                            onChange={(e) => setEditForm({
                              ...editForm,
                              experience_years: parseInt(e.target.value)
                            })}
                            className="border rounded px-2 py-1 text-sm w-20"
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            type="number"
                            value={editForm.consultation_fee}
                            onChange={(e) => setEditForm({
                              ...editForm,
                              consultation_fee: parseFloat(e.target.value)
                            })}
                            className="border rounded px-2 py-1 text-sm w-24"
                          />
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleUpdate(doctor.id)}
                              className="bg-green-600 text-white px-3 py-1
                                         rounded text-sm hover:bg-green-700"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => setEditDoctor(null)}
                              className="bg-gray-200 text-gray-700 px-3 py-1
                                         rounded text-sm hover:bg-gray-300"
                            >
                              Cancel
                            </button>
                          </div>
                        </td>
                      </>
                    ) : (
                      <>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-full bg-blue-100
                                            flex items-center justify-center
                                            text-blue-600 font-semibold">
                              {doctor.email?.charAt(0).toUpperCase()}
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-800">
                                {doctor.email}
                              </p>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className="px-2 py-1 bg-blue-50 text-blue-700
                                           rounded-full text-xs font-medium">
                            {doctor.specialization}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {doctor.experience_years} years
                        </td>
                        <td className="px-6 py-4 text-sm font-medium
                                        text-gray-800">
                          ₹{doctor.consultation_fee}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleEdit(doctor)}
                              className="bg-blue-50 text-blue-600 px-3 py-1
                                         rounded text-sm hover:bg-blue-100"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDeactivate(doctor.id)}
                              className="bg-red-50 text-red-600 px-3 py-1
                                         rounded text-sm hover:bg-red-100"
                            >
                              Deactivate
                            </button>
                          </div>
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>

            {doctors.length === 0 && (
              <div className="text-center py-12 text-gray-400">
                <p className="text-4xl mb-2">👨‍⚕️</p>
                <p>No doctors registered yet</p>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  )
}

export default ManageDoctors