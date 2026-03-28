import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Star } from '@phosphor-icons/react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { toast } from 'sonner';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FeedbackForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    rating: 5,
    category: '',
    feedback_text: ''
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
      const response = await axios.post(`${API}/feedback`, formData);
      toast.success('Thank you for your feedback!');
      setFormData({
        name: '',
        email: '',
        rating: 5,
        category: '',
        feedback_text: ''
      });
    } catch (error) {
      console.error('Feedback error:', error);
      toast.error('Failed to submit feedback. Please try again.');
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
              Client Feedback
            </h1>
            <p className="text-sm" style={{ color: '#5C6661' }}>We value your insights</p>
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
                Share Your Experience
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="name" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Name *</Label>
                  <Input
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full"
                    data-testid="input-name"
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
              </div>
            </div>

            <div>
              <Label htmlFor="rating" className="text-sm font-medium mb-3 block" style={{ color: '#1A1D1C' }}>Rating *</Label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setFormData({ ...formData, rating: star })}
                    className="p-2 transition-transform hover:scale-110"
                    data-testid={`rating-star-${star}`}
                  >
                    <Star
                      size={32}
                      weight={formData.rating >= star ? 'fill' : 'regular'}
                      style={{ color: formData.rating >= star ? '#C16252' : '#E8E5DD' }}
                    />
                  </button>
                ))}
              </div>
            </div>

            <div>
              <Label htmlFor="category" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Feedback Category *</Label>
              <Select
                value={formData.category}
                onValueChange={(value) => setFormData({ ...formData, category: value })}
                required
              >
                <SelectTrigger className="w-full" data-testid="select-category">
                  <SelectValue placeholder="Select a category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="service">Service Quality</SelectItem>
                  <SelectItem value="product">Product Quality</SelectItem>
                  <SelectItem value="support">Customer Support</SelectItem>
                  <SelectItem value="website">Website Experience</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="feedback_text" className="text-sm font-medium mb-2 block" style={{ color: '#1A1D1C' }}>Your Feedback *</Label>
              <Textarea
                id="feedback_text"
                name="feedback_text"
                value={formData.feedback_text}
                onChange={handleChange}
                required
                placeholder="Please share your thoughts, suggestions, or concerns..."
                className="w-full"
                rows={6}
                data-testid="input-feedback-text"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-8 py-4 rounded-full text-white font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#C16252' }}
              data-testid="submit-button"
            >
              {loading ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default FeedbackForm;