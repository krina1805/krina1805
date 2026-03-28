import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from '@phosphor-icons/react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { toast } from 'sonner';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AppointmentBooking = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    patient_name: '',
    email: '',
    phone: '',
    address: '',
    date_of_birth: '',
    appointment_date: '',
    appointment_time: '',
    reason: '',
    medical_history: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/appointments`, formData);
      toast.success('Appointment booked successfully!');
      setFormData({
        patient_name: '',
        email: '',
        phone: '',
        address: '',
        date_of_birth: '',
        appointment_date: '',
        appointment_time: '',
        reason: '',
        medical_history: ''
      });
    } catch (error) {
      console.error('Appointment error:', error);
      toast.error('Failed to book appointment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: '#F9F8F5' }}>
      <header className="backdrop-blur-xl bg-white/70 border-b border-white/40 sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="p-2 rounded-full hover:bg-black/5 transition-colors"
            data-testid="back-button"
          >
            <ArrowLeft size={24} style={{ color: '#1A3629' }} />
          </button>
          <div>
            <h1 className="text-xl font-heading font-medium" style={{ color: '#1A1D1C' }} data-testid="form-title">
              Medical Appointment
            </h1>
            <p className="text-sm" style={{ color: '#5C6661' }}>Schedule your appointment</p>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-8 md:p-12 border"
          style={{ borderColor: '#E8E5DD' }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl tracking-tight font-medium mb-6" style={{ color: '#1A1D1C' }}>
                Patient Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="patient_name" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Patient Name *</Label>
                  <Input
                    id="patient_name"
                    name="patient_name"
                    value={formData.patient_name}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-patient-name"
                  />
                </div>
                <div>
                  <Label htmlFor="date_of_birth" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Date of Birth *</Label>
                  <Input
                    id="date_of_birth"
                    name="date_of_birth"
                    type="date"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-dob"
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Email *</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-email"
                  />
                </div>
                <div>
                  <Label htmlFor="phone" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Phone *</Label>
                  <Input
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-phone"
                  />
                </div>
                <div className="md:col-span-2">
                  <Label htmlFor="address" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Address *</Label>
                  <Textarea
                    id="address"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    required
                    className="w-full"
                    rows={2}
                    data-testid="input-address"
                  />
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl sm:text-3xl tracking-tight font-medium mb-6" style={{ color: '#1A1D1C' }}>
                Appointment Details
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="appointment_date" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Preferred Date *</Label>
                  <Input
                    id="appointment_date"
                    name="appointment_date"
                    type="date"
                    value={formData.appointment_date}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-appointment-date"
                  />
                </div>
                <div>
                  <Label htmlFor="appointment_time" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Preferred Time *</Label>
                  <Input
                    id="appointment_time"
                    name="appointment_time"
                    type="time"
                    value={formData.appointment_time}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-appointment-time"
                  />
                </div>
                <div className="md:col-span-2">
                  <Label htmlFor="reason" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Reason for Visit *</Label>
                  <Textarea
                    id="reason"
                    name="reason"
                    value={formData.reason}
                    onChange={handleChange}
                    required
                    placeholder="Please describe your symptoms or reason for visit..."
                    className="w-full"
                    rows={3}
                    data-testid="input-reason"
                  />
                </div>
                <div className="md:col-span-2">
                  <Label htmlFor="medical_history" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Medical History (Optional)</Label>
                  <Textarea
                    id="medical_history"
                    name="medical_history"
                    value={formData.medical_history}
                    onChange={handleChange}
                    placeholder="Any relevant medical history, allergies, or current medications..."
                    className="w-full"
                    rows={3}
                    data-testid="input-medical-history"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-8 py-4 rounded-full text-white font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#1A3629' }}
              data-testid="submit-button"
            >
              {loading ? 'Booking...' : 'Book Appointment'}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default AppointmentBooking;