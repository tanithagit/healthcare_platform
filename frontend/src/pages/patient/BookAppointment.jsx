import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import {
  getAllDoctors,
  bookAppointment,
  checkSlotAvailability
} from '../../api/appointmentApi'
import { useNavigate } from 'react-router-dom'

const BookAppointment = () => {
  const [doctors, setDoctors] = useState([])
  const [selectedDoctor, setSelectedDoctor] = useState(null)
  const [appointmentDate, setAppointmentDate] = useState('')
  const [reason, setReason] = useState('')
  const [slotStatus, setSlotStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchDoctors()
  }, [])

  const fetchDoctors = async () => {
    try {
      const data = await getAllDoctors()
      setDoctors(data)
    } catch (err) {
      setError('Failed to load doctors')
    }
  }

  const handleCheckSlot = async () => {
    if (!selectedDoctor || !appointmentDate) return
    try {
      const result = await checkSlotAvailability(
        selectedDoctor.id,
        appointmentDate
      )
      setSlotStatus(result)
    } catch (err) {
      setError('Failed to check slot')
    }
  }

  const handleBook = async (e) => {
    e.preventDefault()
    if (!selectedDoctor) {
      setError('Please select a doctor')
      return
    }
    setLoading(true)
    setError('')

    try {
      await bookAppointment({
        doctor_id: selectedDoctor.id,
        appointment_date: appointmentDate,
        reason
      })
      setSuccess('Appointment booked successfully! Check your email.')
      setTimeout(() => navigate('/patient/appointments'), 2000)
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to book appointment'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="space-y-6 max-w-3xl">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Book Appointment
          </h1>
          <p className="text-gray-500 mt-1">
            Select a doctor and choose your time slot
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

        {/* Step 1: Select Doctor */}
        <div className="bg-white rounded-xl shadow-sm border
                        border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Step 1: Select Doctor
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {doctors.map((doctor) => (
              <div
                key={doctor.id}
                onClick={() => setSelectedDoctor(doctor)}
                className={`p-4 rounded-xl border-2 cursor-pointer
                            transition
                  ${selectedDoctor?.id === doctor.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-blue-100
                                  flex items-center justify-center
                                  text-blue-600 font-bold text-lg">
                    {doctor.email?.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">
                      Dr. {doctor.email?.split('@')[0]}
                    </p>
                    <p className="text-sm text-blue-600">
                      {doctor.specialization}
                    </p>
                    <p className="text-sm text-gray-500">
                      💰 ₹{doctor.consultation_fee} •
                      {doctor.experience_years} yrs exp
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Step 2: Select Date & Time */}
        {selectedDoctor && (
          <div className="bg-white rounded-xl shadow-sm border
                          border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Step 2: Select Date & Time
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium
                                  text-gray-700 mb-1">
                  Appointment Date & Time
                </label>
                <div className="flex gap-3">
                  <input
                    type="datetime-local"
                    value={appointmentDate}
                    onChange={(e) => {
                      setAppointmentDate(e.target.value)
                      setSlotStatus(null)
                    }}
                    min={new Date().toISOString().slice(0, 16)}
                    className="flex-1 px-4 py-2.5 border border-gray-300
                               rounded-lg focus:outline-none focus:ring-2
                               focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    onClick={handleCheckSlot}
                    disabled={!appointmentDate}
                    className="px-4 py-2.5 bg-gray-100 text-gray-700
                               rounded-lg hover:bg-gray-200 text-sm
                               font-medium disabled:opacity-50"
                  >
                    Check Slot
                  </button>
                </div>

                {/* Slot Status */}
                {slotStatus && (
                  <div className={`mt-2 p-3 rounded-lg text-sm
                    ${slotStatus.available
                      ? 'bg-green-50 text-green-700'
                      : 'bg-red-50 text-red-700'
                    }`}>
                    {slotStatus.available
                      ? '✅ Slot is available!'
                      : '❌ Slot not available. Choose another time.'
                    }
                  </div>
                )}
              </div>

              {/* Reason */}
              <div>
                <label className="block text-sm font-medium
                                  text-gray-700 mb-1">
                  Reason for Visit
                </label>
                <textarea
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Describe your symptoms or reason..."
                  rows={3}
                  className="w-full px-4 py-2.5 border border-gray-300
                             rounded-lg focus:outline-none focus:ring-2
                             focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Confirm Booking */}
        {selectedDoctor && appointmentDate && (
          <div className="bg-white rounded-xl shadow-sm border
                          border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Step 3: Confirm Booking
            </h2>
            <div className="bg-blue-50 rounded-lg p-4 mb-4 space-y-2">
              <p className="text-sm">
                <span className="font-medium">Doctor:</span>{' '}
                Dr. {selectedDoctor.email?.split('@')[0]}
              </p>
              <p className="text-sm">
                <span className="font-medium">Specialization:</span>{' '}
                {selectedDoctor.specialization}
              </p>
              <p className="text-sm">
                <span className="font-medium">Date & Time:</span>{' '}
                {new Date(appointmentDate).toLocaleString()}
              </p>
              <p className="text-sm">
                <span className="font-medium">Fee:</span>{' '}
                ₹{selectedDoctor.consultation_fee}
              </p>
            </div>
            <button
              onClick={handleBook}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg
                         font-semibold hover:bg-blue-700 transition
                         disabled:opacity-50"
            >
              {loading ? 'Booking...' : '✅ Confirm Appointment'}
            </button>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default BookAppointment