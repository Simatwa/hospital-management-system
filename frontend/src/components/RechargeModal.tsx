import { useState, useEffect } from 'react';
import { CreditCard, DollarSign, Phone, AlertCircle } from 'lucide-react';
import { api } from '../lib/axios';
import toast from 'react-hot-toast';
import Modal from './ui/Modal';

interface PaymentAccountDetails {
  name: string;
  paybill_number: string;
  account_number: string;
  details: string;
}

interface RechargeModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

export default function RechargeModal({ onClose, onSuccess }: RechargeModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [amount, setAmount] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [paymentAccounts, setPaymentAccounts] = useState<PaymentAccountDetails[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<PaymentAccountDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPaymentAccounts();
  }, []);

  const fetchPaymentAccounts = async () => {
    try {
      const response = await api.get('/payment-account-details');
      setPaymentAccounts(response.data);
      if (response.data.length > 0) {
        setSelectedAccount(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching payment accounts:', error);
      toast.error('Failed to load payment details');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
      toast.error('Please enter a valid amount');
      return;
    }

    if (!phoneNumber) {
      toast.error('Please enter your M-PESA phone number');
      return;
    }

    if (!/^\+?[\d\s-]{10,}$/.test(phoneNumber)) {
      toast.error('Please enter a valid phone number');
      return;
    }

    setIsSubmitting(true);
    try {
      await api.post('/send-mpesa-payment-popup', {
        phone_number: phoneNumber,
        amount: Number(amount)
      });
      
      toast.success('M-PESA payment request sent. Please check your phone for the payment prompt.', {
        duration: 5000,
      });
    } catch (error) {
      console.error('Error sending M-PESA request:', error);
      toast.error('Failed to send M-PESA payment request');
    } finally {
      setIsSubmitting(false);
    }
  };

  const quickAmounts = [1000, 2000, 5000, 10000];

  if (loading) {
    return (
      <Modal
        title="Loading"
        onClose={onClose}
        showClose={false}
        className="max-w-md"
      >
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading payment details...</p>
        </div>
      </Modal>
    );
  }

  if (paymentAccounts.length === 0) {
    return (
      <Modal
        title="Payment Not Available"
        onClose={onClose}
        className="max-w-md"
      >
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto" />
          <p className="mt-2 text-gray-500">Payment services are currently unavailable. Please try again later.</p>
        </div>
      </Modal>
    );
  }

  return (
    <Modal
      title="M-PESA Payment"
      onClose={onClose}
      className="max-w-md"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Amount (Ksh)
          </label>
          <div className="relative">
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              placeholder="Enter amount"
              min="1"
              required
            />
            <DollarSign className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quick Amounts
          </label>
          <div className="grid grid-cols-2 gap-2">
            {quickAmounts.map((quickAmount) => (
              <button
                key={quickAmount}
                type="button"
                onClick={() => setAmount(quickAmount.toString())}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left"
              >
                Ksh {quickAmount.toLocaleString()}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            M-PESA Phone Number
          </label>
          <div className="relative">
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              placeholder="Enter M-PESA number"
              required
            />
            <Phone className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>
        </div>

        <div className="bg-primary-50 p-4 rounded-lg space-y-4">
          <h3 className="text-sm font-medium text-primary flex items-center gap-2">
            <CreditCard className="h-5 w-5" />
            Payment Instructions
          </h3>
          <div className="space-y-2 text-sm text-gray-600">
            <p className="font-medium">{selectedAccount?.name}</p>
            <p>Paybill Number: {selectedAccount?.paybill_number}</p>
            <p>Account Number: {selectedAccount?.account_number}</p>
            <p className="text-xs italic">{selectedAccount?.details}</p>
          </div>
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <button
            type="button"
            onClick={onClose}
            className="px-6 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 text-white bg-primary hover:bg-primary-600 rounded-lg transition-colors disabled:opacity-50"
          >
            {isSubmitting ? 'Processing...' : 'Pay with M-PESA'}
          </button>
        </div>
      </form>
    </Modal>
  );
}