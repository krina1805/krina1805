import React, { useState, useEffect, useRef } from 'react';
import { PaperPlaneTilt, Heart, Barbell, FirstAid, Leaf } from '@phosphor-icons/react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HealthcareChat = () => {
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
        const response = await axios.get(`${API}/chat/history/${sessionId}/healthcare`);
        if (response.data.messages && response.data.messages.length > 0) {
          setMessages(response.data.messages);
        } else {
          setMessages([{
            role: 'assistant',
            content: 'Hello! I\'m your healthcare AI assistant. I can help you with:\n\n• Weight management and healthy weight loss strategies\n• Home remedies for common ailments\n• Exercise recommendations and fitness advice\n• General health and wellness guidance\n• Nutrition tips and dietary suggestions\n\nHow can I assist you today?',
            timestamp: new Date().toISOString()
          }]);
        }
      } catch (error) {
        console.error('Failed to load history:', error);
        setMessages([{
          role: 'assistant',
          content: 'Hello! I\'m your healthcare AI assistant. I can help you with weight management, home remedies, exercise recommendations, and general health advice. How can I assist you today?',
          timestamp: new Date().toISOString()
        }]);
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
        agent_type: 'healthcare'
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

  const quickPrompts = [
    { icon: Heart, text: 'Weight loss tips', prompt: 'What are some effective tips for healthy weight loss?' },
    { icon: Barbell, text: 'Exercise advice', prompt: 'Can you recommend exercises for beginners?' },
    { icon: FirstAid, text: 'Home remedies', prompt: 'What are some home remedies for common cold?' },
    { icon: Leaf, text: 'Nutrition tips', prompt: 'What should I eat for a balanced diet?' }
  ];

  const handleQuickPrompt = (prompt) => {
    setInput(prompt);
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: '#F9F8F5' }}>
      {/* Header */}
      <header className="backdrop-blur-xl bg-white/70 border-b border-white/40 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 py-6">
          <div className="flex items-center gap-4">
            <div 
              className="w-14 h-14 rounded-full flex items-center justify-center flex-shrink-0"
              style={{ backgroundColor: '#C1625215' }}
            >
              <Heart size={28} weight="duotone" style={{ color: '#C16252' }} />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-heading font-light tracking-tight" style={{ color: '#1A1D1C' }} data-testid="chat-title">
                Healthcare AI Assistant
              </h1>
              <p className="text-sm" style={{ color: '#5C6661' }}>Your personal health & wellness guide</p>
            </div>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 1 && messages[0].role === 'assistant' && (
            <div className="mb-8">
              <p className="text-sm font-medium mb-4" style={{ color: '#5C6661' }}>Quick questions to get started:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {quickPrompts.map((item, index) => {
                  const IconComponent = item.icon;
                  return (
                    <motion.button
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      onClick={() => handleQuickPrompt(item.prompt)}
                      className="flex items-center gap-3 p-4 bg-white rounded-xl border hover:shadow-md transition-all duration-300 text-left"
                      style={{ borderColor: '#E8E5DD' }}
                      data-testid={`quick-prompt-${index}`}
                    >
                      <div 
                        className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
                        style={{ backgroundColor: '#1A362915' }}
                      >
                        <IconComponent size={20} weight="duotone" style={{ color: '#1A3629' }} />
                      </div>
                      <span className="text-sm font-medium" style={{ color: '#1A1D1C' }}>{item.text}</span>
                    </motion.button>
                  );
                })}
              </div>
            </div>
          )}

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
                    ? 'bg-[#1A3629] text-white chat-bubble-user'
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
                  <div className="w-2 h-2 rounded-full bg-[#1A3629] animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-[#1A3629] animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-[#1A3629] animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t" style={{ borderColor: '#E8E5DD', background: '#FFFFFF' }}>
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about weight loss, home remedies, exercises, nutrition..."
              className="flex-1 px-4 py-3 rounded-xl border text-base focus:ring-2 focus:ring-[#1A3629]/20 focus:border-[#1A3629] transition-all outline-none"
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
              className="px-8 py-3 rounded-full text-white font-medium transition-all duration-300 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg"
              style={{ backgroundColor: '#1A3629' }}
              onMouseEnter={(e) => !loading && !(!input.trim()) && (e.currentTarget.style.backgroundColor = '#264D3A')}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#1A3629'}
              data-testid="send-button"
            >
              <PaperPlaneTilt size={20} weight="fill" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </div>
          <p className="text-xs mt-3 text-center" style={{ color: '#8A9A86' }}>AI-powered healthcare advice. Always consult with healthcare professionals for serious concerns.</p>
        </div>
      </div>
    </div>
  );
};

export default HealthcareChat;