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

const JobApplication = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    address: '',
    position_applied: '',
    education: '',
    experience: '',
    skills: '',
    reference_name: '',
    reference_contact: '',
    reference_relationship: ''
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
      const response = await axios.post(`${API}/job-application`, formData);
      toast.success('Application submitted successfully!');
      setFormData({
        full_name: '',
        email: '',
        phone: '',
        address: '',
        position_applied: '',
        education: '',
        experience: '',
        skills: '',
        reference_name: '',
        reference_contact: '',
        reference_relationship: ''
      });
    } catch (error) {
      console.error('Application error:', error);
      toast.error('Failed to submit application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: '#F9F8F5' }}>
      {/* Header */}
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
              Job Application
            </h1>
            <p className="text-sm" style={{ color: '#5C6661' }}>Submit your application details</p>
          </div>
        </div>
      </header>

      {/* Form */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-8 md:p-12 border"
          style={{ borderColor: '#E8E5DD' }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information */}
            <div>
              <h2 className="text-2xl sm:text-3xl tracking-tight font-medium mb-6" style={{ color: '#1A1D1C' }}>
                Personal Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="full_name" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Full Name *</Label>
                  <Input
                    id="full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-full-name"
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
                <div>
                  <Label htmlFor="position_applied" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Position Applied *</Label>
                  <Input
                    id="position_applied"
                    name="position_applied"
                    value={formData.position_applied}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-position"
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

            {/* Education & Experience */}
            <div>
              <h2 className="text-2xl sm:text-3xl tracking-tight font-medium mb-6" style={{ color: '#1A1D1C' }}>
                Education & Experience
              </h2>
              <div className="space-y-6">
                <div>
                  <Label htmlFor="education" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Education Background *</Label>
                  <Textarea
                    id="education"
                    name="education"
                    value={formData.education}
                    onChange={handleChange}
                    required
                    placeholder="List your educational qualifications..."
                    className="w-full"
                    rows={3}
                    data-testid="input-education"
                  />
                </div>
                <div>
                  <Label htmlFor="experience" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Work Experience *</Label>
                  <Textarea
                    id="experience"
                    name="experience"
                    value={formData.experience}
                    onChange={handleChange}
                    required
                    placeholder="Describe your work experience..."
                    className="w-full"
                    rows={3}
                    data-testid="input-experience"
                  />
                </div>
                <div>
                  <Label htmlFor="skills" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Skills *</Label>
                  <Textarea
                    id="skills"
                    name="skills"
                    value={formData.skills}
                    onChange={handleChange}
                    required
                    placeholder="List your relevant skills..."
                    className="w-full"
                    rows={3}
                    data-testid="input-skills"
                  />
                </div>
              </div>
            </div>

            {/* References */}
            <div>
              <h2 className="text-2xl sm:text-3xl tracking-tight font-medium mb-6" style={{ color: '#1A1D1C' }}>
                Professional Reference
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <Label htmlFor="reference_name" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Reference Name *</Label>
                  <Input
                    id="reference_name"
                    name="reference_name"
                    value={formData.reference_name}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-reference-name"
                  />
                </div>
                <div>
                  <Label htmlFor="reference_contact" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Reference Contact *</Label>
                  <Input
                    id="reference_contact"
                    name="reference_contact"
                    value={formData.reference_contact}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-reference-contact"
                  />
                </div>
                <div>
                  <Label htmlFor="reference_relationship" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Relationship *</Label>
                  <Input
                    id="reference_relationship"
                    name="reference_relationship"
                    value={formData.reference_relationship}
                    onChange={handleChange}
                    required
                    placeholder="e.g., Former Manager"
                    className="w-full"
                    data-testid="input-reference-relationship"
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full px-8 py-4 rounded-full text-white font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#1A3629' }}
              data-testid="submit-button"
            >
              {loading ? 'Submitting...' : 'Submit Application'}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default JobApplication;