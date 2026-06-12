import axios from './axios'

export const createPrescription = async (data) => {
  const response = await axios.post('/api/prescriptions/', data)
  return response.data
}

export const getMyPrescriptions = async () => {
  const response = await axios.get('/api/prescriptions/my')
  return response.data
}

export const getPrescriptionsByAppointment = async (appointmentId) => {
  const response = await axios.get(
    `/api/prescriptions/appointment/${appointmentId}`
  )
  return response.data
}

export const createMedicalRecord = async (data) => {
  const response = await axios.post('/api/medical-records/', data)
  return response.data
}

export const getMyMedicalRecords = async () => {
  const response = await axios.get('/api/medical-records/my')
  return response.data
}

export const getDoctorMedicalRecords = async () => {
  const response = await axios.get('/api/medical-records/doctor/my')
  return response.data
}