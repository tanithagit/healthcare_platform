import axios from './axios'

export const getMyInvoices = async () => {
  const response = await axios.get('/api/billing/my')
  return response.data
}

export const getInvoiceByAppointment = async (appointmentId) => {
  const response = await axios.get(
    `/api/billing/appointment/${appointmentId}`
  )
  return response.data
}

export const getAllInvoices = async () => {
  const response = await axios.get('/api/billing/')
  return response.data
}

export const markInvoicePaid = async (invoiceId) => {
  const response = await axios.put(`/api/billing/mark-paid/${invoiceId}`)
  return response.data
}

export const createCheckoutSession = async (invoiceId) => {
  const response = await axios.post(`/api/billing/checkout/${invoiceId}`)
  return response.data
}