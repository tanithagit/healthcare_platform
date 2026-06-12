import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import {
  getMyMedicalRecords,
  getMyPrescriptions
} from '../../api/prescriptionApi'

const MedicalHistory = () => {
  const [records, setRecords] = useState([])
  const [prescriptions, setPrescriptions] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('records')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [recordsData, prescriptionsData] = await Promise.all([
        getMyMedicalRecords(),
        getMyPrescriptions()
      ])
      setRecords(recordsData)
      setPrescriptions(prescriptionsData)
    } catch (err) {
      console.error('Failed to load medical history')
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
            Medical History
          </h1>
          <p className="text-gray-500 mt-1">
            Your complete medical records and prescriptions
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('records')}
            className={`px-5 py-2.5 rounded-lg text-sm font-medium
                        transition
              ${activeTab === 'records'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
          >
            📋 Medical Records ({records.length})
          </button>
          <button
            onClick={() => setActiveTab('prescriptions')}
            className={`px-5 py-2.5 rounded-lg text-sm font-medium
                        transition
              ${activeTab === 'prescriptions'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
          >
            💊 Prescriptions ({prescriptions.length})
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10
                            border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Medical Records Tab */}
            {activeTab === 'records' && (
              <div className="space-y-4">
                {records.length === 0 ? (
                  <div className="bg-white rounded-xl p-12
                                  text-center text-gray-400">
                    <p className="text-4xl mb-2">📋</p>
                    <p>No medical records yet</p>
                  </div>
                ) : (
                  records.map((record) => (
                    <div key={record.id}
                      className="bg-white rounded-xl shadow-sm
                                 border border-gray-100 p-6">
                      <div className="flex items-start justify-between">
                        <div className="space-y-2 flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xl">📋</span>
                            <h3 className="font-semibold text-gray-800">
                              Dr. {record.doctor_email?.split('@')[0]}
                            </h3>
                          </div>
                          <div className="bg-blue-50 px-4 py-3
                                          rounded-lg">
                            <p className="text-sm font-semibold
                                          text-blue-800">
                              Diagnosis
                            </p>
                            <p className="text-sm text-blue-700 mt-0.5">
                              {record.diagnosis}
                            </p>
                          </div>
                          {record.notes && (
                            <div className="bg-gray-50 px-4 py-3
                                            rounded-lg">
                              <p className="text-sm font-semibold
                                            text-gray-600">
                                Notes
                              </p>
                              <p className="text-sm text-gray-600 mt-0.5">
                                {record.notes}
                              </p>
                            </div>
                          )}
                          <p className="text-xs text-gray-400">
                            📅 {new Date(record.created_at)
                              .toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Prescriptions Tab */}
            {activeTab === 'prescriptions' && (
              <div className="space-y-4">
                {prescriptions.length === 0 ? (
                  <div className="bg-white rounded-xl p-12
                                  text-center text-gray-400">
                    <p className="text-4xl mb-2">💊</p>
                    <p>No prescriptions yet</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2
                                  gap-4">
                    {prescriptions.map((prescription) => (
                      <div key={prescription.id}
                        className="bg-white rounded-xl shadow-sm
                                   border border-gray-100 p-5">
                        <div className="flex items-start gap-3">
                          <div className="text-2xl">💊</div>
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-800">
                              {prescription.medicine_name}
                            </h3>
                            <div className="mt-2 space-y-1">
                              <p className="text-sm text-gray-600">
                                <span className="font-medium">
                                  Dosage:
                                </span>{' '}
                                {prescription.dosage}
                              </p>
                              {prescription.instructions && (
                                <p className="text-sm text-gray-600">
                                  <span className="font-medium">
                                    Instructions:
                                  </span>{' '}
                                  {prescription.instructions}
                                </p>
                              )}
                              {prescription.duration_days && (
                                <p className="text-sm text-gray-600">
                                  <span className="font-medium">
                                    Duration:
                                  </span>{' '}
                                  {prescription.duration_days} days
                                </p>
                              )}
                            </div>
                            <p className="text-xs text-gray-400 mt-2">
                              📅 {new Date(prescription.created_at)
                                .toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </Layout>
  )
}

export default MedicalHistory