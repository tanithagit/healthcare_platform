import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import axios from '../../api/axios'

const DoctorPrescriptions = () => {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchRecords()
  }, [])

  const fetchRecords = async () => {
    try {
      const response = await axios.get('/api/medical-records/doctor/my')
      setRecords(response.data)
    } catch (err) {
      setError('Failed to load medical records')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Medical Records & Prescriptions
          </h1>
          <p className="text-gray-500 mt-1">
            View all records you have created
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
        ) : records.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center
                          text-gray-400">
            <p className="text-4xl mb-2">📋</p>
            <p>No medical records created yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {records.map((record) => (
              <div key={record.id}
                className="bg-white rounded-xl shadow-sm border
                           border-gray-100 p-6">
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">📋</span>
                      <h3 className="font-semibold text-gray-800">
                        Patient: {record.patient_email}
                      </h3>
                    </div>
                    <div className="bg-blue-50 px-4 py-2
                                    rounded-lg inline-block">
                      <p className="text-sm font-medium text-blue-800">
                        Diagnosis: {record.diagnosis}
                      </p>
                    </div>
                    {record.notes && (
                      <p className="text-sm text-gray-600">
                        📝 Notes: {record.notes}
                      </p>
                    )}
                    <p className="text-xs text-gray-400">
                      Created: {new Date(record.created_at)
                        .toLocaleDateString()}
                    </p>
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

export default DoctorPrescriptions