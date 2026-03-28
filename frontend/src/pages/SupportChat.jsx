import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, PaperPlaneTilt } from '@phosphor-icons/react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SupportChat = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await axios.get(`${API}/chat/history/${sessionId}/support`);
        if (response.data.messages && response.data.messages.length > 0) {
          setMessages(response.data.messages);
        } else {
          setMessages([{
            role: 'assistant',
            content: 'Hello! I\'m your customer support assistant. I\'m here to help answer your questions, resolve issues, and provide solutions. How can I help you today?',
            timestamp: new Date().toISOString()
          }]);
        }
      } catch (error) {
        console.error('Failed to load history:', error);
      }
    };
    loadHistory();
  }, [sessionId]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        session_id: sessionId,
        message: input,
        agent_type: 'support'
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: response.data.timestamp
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: '#F9F8F5' }}>
      <header className="backdrop-blur-xl bg-white/70 border-b border-white/40 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="p-2 rounded-full hover:bg-black/5 transition-colors"
            data-testid="back-button"
          >
            <ArrowLeft size={24} style={{ color: '#1A3629' }} />
          </button>
          <div className="flex items-center gap-3">
            <img 
              src="https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/8f900730b6f0bdc3b684ee4b5fabfa41ba5b5402cabb1ecc7d5370b8fd439d65.png" 
              alt="Support" 
              className="w-10 h-10 rounded-full object-cover"
            />
            <div>
              <h1 className="text-xl font-heading font-medium" style={{ color: '#1A1D1C' }} data-testid="chat-title">
                Customer Support
              </h1>
              <p className="text-sm" style={{ color: '#5C6661' }}>We're here to help</p>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              data-testid={`message-${message.role}-${index}`}
            >
              <div
                className={`max-w-[80%] p-6 shadow-sm ${
                  message.role === 'user'
                    ? 'bg-[#8A9A86] text-white chat-bubble-user'
                    : 'bg-[#F1EFEA] text-[#1A1D1C] chat-bubble-bot border border-[#E8E5DD]/50'
                }`}
              >
                <p className="text-base leading-relaxed whitespace-pre-wrap">{message.content}</p>
              </div>
            </motion.div>
          ))}
          {loading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="bg-[#F1EFEA] text-[#1A1D1C] chat-bubble-bot border border-[#E8E5DD]/50 p-6 shadow-sm">
                <div className="flex gap-2">
                  <div className="w-2 h-2 rounded-full bg-[#8A9A86] animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-[#8A9A86] animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-[#8A9A86] animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="border-t" style={{ borderColor: '#E8E5DD', background: '#FFFFFF' }}>
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your issue or question..."
              className="flex-1 px-4 py-3 rounded-xl border text-base focus:ring-2 focus:ring-[#8A9A86]/20 focus:border-[#8A9A86] transition-all outline-none"
              style={{ 
                backgroundColor: 'white',
                borderColor: '#E8E5DD',
                color: '#1A1D1C'
              }}
              disabled={loading}
              data-testid="chat-input"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="px-8 py-3 rounded-full text-white font-medium transition-all duration-300 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#8A9A86' }}
              data-testid="send-button"
            >
              <PaperPlaneTilt size={20} weight="fill" />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SupportChat;