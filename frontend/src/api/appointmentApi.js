import axios from './axios'

export const bookAppointment = async (data) => {
  const response = await axios.post('/api/appointments/', data)
  return response.data
}

export const getMyAppointments = async () => {
  const response = await axios.get('/api/appointments/my')
  return response.data
}

export const getDoctorAppointments = async () => {
  const response = await axios.get('/api/appointments/doctor/my')
  return response.data
}

export const getAllAppointments = async () => {
  const response = await axios.get('/api/appointments/')
  return response.data
}

export const updateAppointmentStatus = async (id, data) => {
  const response = await axios.put(`/api/appointments/${id}/status`, data)
  return response.data
}

export const cancelAppointment = async (id) => {
  const response = await axios.put(`/api/appointments/${id}/cancel`)
  return response.data
}

export const checkSlotAvailability = async (doctorId, date) => {
  const response = await axios.get('/api/appointments/check-slot', {
    params: { doctor_id: doctorId, appointment_date: date }
  })
  return response.data
}

export const getAllDoctors = async () => {
  const response = await axios.get('/api/doctors/')
  return response.data
}