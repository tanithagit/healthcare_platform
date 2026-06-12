import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import { getMyInvoices, markInvoicePaid } from '../../api/billingApi'

const Billing = () => {
  const [invoices, setInvoices] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [payingId, setPayingId] = useState(null)

  useEffect(() => {
    fetchInvoices()
  }, [])

  const fetchInvoices = async () => {
    try {
      const data = await getMyInvoices()
      setInvoices(data)
    } catch (err) {
      setError('Failed to load invoices')
    } finally {
      setLoading(false)
    }
  }

  const handlePay = async (invoiceId) => {
    setPayingId(invoiceId)
    try {
      await markInvoicePaid(invoiceId)
      setSuccess('Payment successful! Receipt sent to your email.')
      fetchInvoices()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Payment failed. Please try again.')
    } finally {
      setPayingId(null)
    }
  }

  const getStatusColor = (status) => {
    if (status === 'paid') return 'bg-green-100 text-green-700'
    if (status === 'pending') return 'bg-yellow-100 text-yellow-700'
    if (status === 'failed') return 'bg-red-100 text-red-700'
    return 'bg-gray-100 text-gray-700'
  }

  const totalPaid = invoices
    .filter(i => i.payment_status === 'paid')
    .reduce((sum, i) => sum + i.amount, 0)

  const totalPending = invoices
    .filter(i => i.payment_status === 'pending')
    .reduce((sum, i) => sum + i.amount, 0)

  return (
    <Layout>
      <div className="space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Billing & Payments
          </h1>
          <p className="text-gray-500 mt-1">
            Manage your consultation payments
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

        {/* Summary Cards */}
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Total Paid</p>
            <p className="text-3xl font-bold text-green-600 mt-1">
              ₹{totalPaid}
            </p>
            <p className="text-xs text-gray-400 mt-1">✅ Completed</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6
                          border border-gray-100">
            <p className="text-sm text-gray-500">Pending Amount</p>
            <p className="text-3xl font-bold text-yellow-600 mt-1">
              ₹{totalPending}
            </p>
            <p className="text-xs text-gray-400 mt-1">⏳ Due</p>
          </div>
        </div>

        {/* Invoices List */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10
                            border-b-2 border-blue-600"></div>
          </div>
        ) : invoices.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center
                          text-gray-400">
            <p className="text-4xl mb-2">💳</p>
            <p>No invoices yet</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border
                          border-gray-100 overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs
                                  font-semibold text-gray-500
                                  uppercase">Invoice</th>
                  <th className="px-6 py-4 text-left text-xs
                                  font-semibold text-gray-500
                                  uppercase">Appointment</th>
                  <th className="px-6 py-4 text-left text-xs
                                  font-semibold text-gray-500
                                  uppercase">Amount</th>
                  <th className="px-6 py-4 text-left text-xs
                                  font-semibold text-gray-500
                                  uppercase">Status</th>
                  <th className="px-6 py-4 text-left text-xs
                                  font-semibold text-gray-500
                                  uppercase">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {invoices.map((invoice) => (
                  <tr key={invoice.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium
                                    text-gray-800">
                      #INV-{invoice.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      APT-{invoice.appointment_id}
                    </td>
                    <td className="px-6 py-4 text-sm font-bold
                                    text-gray-800">
                      ₹{invoice.amount}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full
                                       text-xs font-medium
                                       ${getStatusColor(
                                         invoice.payment_status
                                       )}`}>
                        {invoice.payment_status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {invoice.payment_status === 'pending' ? (
                        <button
                          onClick={() => handlePay(invoice.id)}
                          disabled={payingId === invoice.id}
                          className="bg-blue-600 text-white px-4
                                     py-1.5 rounded-lg text-sm
                                     hover:bg-blue-700
                                     disabled:opacity-50"
                        >
                          {payingId === invoice.id
                            ? 'Processing...'
                            : 'Pay Now'
                          }
                        </button>
                      ) : (
                        <span className="text-sm text-gray-400">
                          {invoice.paid_at
                            ? new Date(invoice.paid_at)
                              .toLocaleDateString()
                            : 'Paid'
                          }
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default Billing