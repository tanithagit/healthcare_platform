import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import {
  getDoctorAppointments,
  updateAppointmentStatus
} from '../../api/appointmentApi'
import { createMedicalRecord } from '../../api/prescriptionApi'
import axios from '../../api/axios'

const DoctorAppointments = () => {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [selectedApt, setSelectedApt] = useState(null)
  const [showRecordForm, setShowRecordForm] = useState(false)
  const [recordForm, setRecordForm] = useState({
    diagnosis: '',
    notes: ''
  })
  const [showPrescriptionForm, setShowPrescriptionForm] = useState(false)
  const [prescriptionForm, setPrescriptionForm] = useState({
    medicine_name: '',
    dosage: '',
    instructions: '',
    duration_days: 7
  })

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

  const handleStatusUpdate = async (aptId, status) => {
    try {
      await updateAppointmentStatus(aptId, { status })
      setSuccess(`Appointment marked as ${status}`)
      fetchAppointments()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Failed to update status')
    }
  }

  const handleCreateRecord = async (e) => {
    e.preventDefault()
    try {
      await createMedicalRecord({
        appointment_id: selectedApt.id,
        ...recordForm
      })
      setSuccess('Medical record created successfully!')
      setShowRecordForm(false)
      setRecordForm({ diagnosis: '', notes: '' })
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to create medical record'
      )
    }
  }

  const handleCreatePrescription = async (e) => {
    e.preventDefault()
    try {
      await axios.post('/api/prescriptions/', {
        appointment_id: selectedApt.id,
        ...prescriptionForm
      })
      setSuccess('Prescription created successfully!')
      setShowPrescriptionForm(false)
      setPrescriptionForm({
        medicine_name: '',
        dosage: '',
        instructions: '',
        duration_days: 7
      })
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Failed to create prescription')
    }
  }

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
            My Appointments
          </h1>
          <p className="text-gray-500 mt-1">
            Manage your patient appointments
          </p>
        </div>

        {/* Messages */}
        {error && (
          <div className="bg-red-50 border border-red-200
                          text-red-600 rounded-lg p-4">
            ❌ {error}
          </div>
        )}
        {success && (
          <div className="bg-green-50 border border-green-200
                          text-green-600 rounded-lg p-4">
            ✅ {success}
          </div>
        )}

        {/* Appointments List */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10
                            border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="space-y-4">
            {appointments.length === 0 ? (
              <div className="bg-white rounded-xl p-12 text-center
                              text-gray-400">
                <p className="text-4xl mb-2">📅</p>
                <p>No appointments yet</p>
              </div>
            ) : (
              appointments.map((apt) => (
                <div key={apt.id}
                  className="bg-white rounded-xl shadow-sm border
                             border-gray-100 p-6">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-gray-800">
                          Patient: {apt.patient_email}
                        </h3>
                        <span className={`px-2 py-0.5 rounded-full
                                         text-xs font-medium
                                         ${getStatusColor(apt.status)}`}>
                          {apt.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500">
                        📅 {new Date(apt.appointment_date)
                          .toLocaleString()}
                      </p>
                      {apt.reason && (
                        <p className="text-sm text-gray-600">
                          📋 Reason: {apt.reason}
                        </p>
                      )}
                      {apt.notes && (
                        <p className="text-sm text-gray-600">
                          📝 Notes: {apt.notes}
                        </p>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-2">
                      {apt.status === 'scheduled' && (
                        <>
                          <button
                            onClick={() => {
                              setSelectedApt(apt)
                              setShowRecordForm(true)
                              setShowPrescriptionForm(false)
                            }}
                            className="bg-purple-50 text-purple-600
                                       px-3 py-1.5 rounded-lg text-sm
                                       hover:bg-purple-100"
                          >
                            📋 Add Record
                          </button>
                          <button
                            onClick={() => {
                              setSelectedApt(apt)
                              setShowPrescriptionForm(true)
                              setShowRecordForm(false)
                            }}
                            className="bg-blue-50 text-blue-600
                                       px-3 py-1.5 rounded-lg text-sm
                                       hover:bg-blue-100"
                          >
                            💊 Prescribe
                          </button>
                          <button
                            onClick={() => handleStatusUpdate(
                              apt.id, 'completed'
                            )}
                            className="bg-green-600 text-white
                                       px-3 py-1.5 rounded-lg text-sm
                                       hover:bg-green-700"
                          >
                            ✅ Complete
                          </button>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Medical Record Form */}
                  {showRecordForm && selectedApt?.id === apt.id && (
                    <div className="mt-4 p-4 bg-purple-50 rounded-lg
                                    border border-purple-200">
                      <h4 className="font-semibold text-purple-800 mb-3">
                        📋 Create Medical Record
                      </h4>
                      <form onSubmit={handleCreateRecord}
                        className="space-y-3">
                        <div>
                          <label className="text-sm font-medium
                                           text-gray-700">
                            Diagnosis *
                          </label>
                          <input
                            value={recordForm.diagnosis}
                            onChange={(e) => setRecordForm({
                              ...recordForm,
                              diagnosis: e.target.value
                            })}
                            required
                            placeholder="Enter diagnosis"
                            className="w-full mt-1 px-3 py-2 border
                                       rounded-lg text-sm focus:outline-none
                                       focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium
                                           text-gray-700">
                            Notes
                          </label>
                          <textarea
                            value={recordForm.notes}
                            onChange={(e) => setRecordForm({
                              ...recordForm,
                              notes: e.target.value
                            })}
                            placeholder="Additional notes"
                            rows={3}
                            className="w-full mt-1 px-3 py-2 border
                                       rounded-lg text-sm focus:outline-none
                                       focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                        <div className="flex gap-2">
                          <button type="submit"
                            className="bg-purple-600 text-white px-4
                                       py-2 rounded-lg text-sm
                                       hover:bg-purple-700">
                            Save Record
                          </button>
                          <button
                            type="button"
                            onClick={() => setShowRecordForm(false)}
                            className="bg-gray-200 text-gray-700 px-4
                                       py-2 rounded-lg text-sm
                                       hover:bg-gray-300">
                            Cancel
                          </button>
                        </div>
                      </form>
                    </div>
                  )}

                  {/* Prescription Form */}
                  {showPrescriptionForm && selectedApt?.id === apt.id && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg
                                    border border-blue-200">
                      <h4 className="font-semibold text-blue-800 mb-3">
                        💊 Add Prescription
                      </h4>
                      <form onSubmit={handleCreatePrescription}
                        className="space-y-3">
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="text-sm font-medium
                                             text-gray-700">
                              Medicine Name *
                            </label>
                            <input
                              value={prescriptionForm.medicine_name}
                              onChange={(e) => setPrescriptionForm({
                                ...prescriptionForm,
                                medicine_name: e.target.value
                              })}
                              required
                              placeholder="e.g. Paracetamol"
                              className="w-full mt-1 px-3 py-2 border
                                         rounded-lg text-sm
                                         focus:outline-none
                                         focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                          <div>
                            <label className="text-sm font-medium
                                             text-gray-700">
                              Dosage *
                            </label>
                            <input
                              value={prescriptionForm.dosage}
                              onChange={(e) => setPrescriptionForm({
                                ...prescriptionForm,
                                dosage: e.target.value
                              })}
                              required
                              placeholder="e.g. 500mg"
                              className="w-full mt-1 px-3 py-2 border
                                         rounded-lg text-sm
                                         focus:outline-none
                                         focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="text-sm font-medium
                                             text-gray-700">
                              Instructions
                            </label>
                            <input
                              value={prescriptionForm.instructions}
                              onChange={(e) => setPrescriptionForm({
                                ...prescriptionForm,
                                instructions: e.target.value
                              })}
                              placeholder="e.g. After meals"
                              className="w-full mt-1 px-3 py-2 border
                                         rounded-lg text-sm
                                         focus:outline-none
                                         focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                          <div>
                            <label className="text-sm font-medium
                                             text-gray-700">
                              Duration (days)
                            </label>
                            <input
                              type="number"
                              value={prescriptionForm.duration_days}
                              onChange={(e) => setPrescriptionForm({
                                ...prescriptionForm,
                                duration_days: parseInt(e.target.value)
                              })}
                              className="w-full mt-1 px-3 py-2 border
                                         rounded-lg text-sm
                                         focus:outline-none
                                         focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <button type="submit"
                            className="bg-blue-600 text-white px-4
                                       py-2 rounded-lg text-sm
                                       hover:bg-blue-700">
                            Save Prescription
                          </button>
                          <button
                            type="button"
                            onClick={() => setShowPrescriptionForm(false)}
                            className="bg-gray-200 text-gray-700 px-4
                                       py-2 rounded-lg text-sm
                                       hover:bg-gray-300">
                            Cancel
                          </button>
                        </div>
                      </form>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </Layout>
  )
}

export default DoctorAppointments