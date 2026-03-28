import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Heart, 
  Briefcase, 
  Headset, 
  ChatCircleDots, 
  Calendar, 
  UserCircle 
} from '@phosphor-icons/react';
import { motion } from 'framer-motion';

const agents = [
  {
    id: 'healthcare',
    title: 'Healthcare AI',
    description: 'Get personalized advice on weight loss, home remedies, exercises, and general health guidance.',
    icon: Heart,
    path: '/healthcare',
    color: '#C16252',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/8f900730b6f0bdc3b684ee4b5fabfa41ba5b5402cabb1ecc7d5370b8fd439d65.png'
  },
  {
    id: 'job-application',
    title: 'Job Application',
    description: 'Submit your job application with personal details, education, and references.',
    icon: Briefcase,
    path: '/job-application',
    color: '#1A3629',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/21c199f557f77f2442e9433d9eb563e6097176f37c7729122d5323fbbeb4d559.png'
  },
  {
    id: 'support',
    title: 'Customer Support',
    description: 'Get help with your questions, resolve issues, and find solutions quickly.',
    icon: Headset,
    path: '/support',
    color: '#8A9A86',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/8f900730b6f0bdc3b684ee4b5fabfa41ba5b5402cabb1ecc7d5370b8fd439d65.png'
  },
  {
    id: 'feedback',
    title: 'Client Feedback',
    description: 'Share your valuable feedback and help us improve our services.',
    icon: ChatCircleDots,
    path: '/feedback',
    color: '#C16252',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/8f900730b6f0bdc3b684ee4b5fabfa41ba5b5402cabb1ecc7d5370b8fd439d65.png'
  },
  {
    id: 'appointments',
    title: 'Medical Appointments',
    description: 'Schedule your medical appointment with ease. We\'ll collect all necessary information.',
    icon: Calendar,
    path: '/appointments',
    color: '#1A3629',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/21c199f557f77f2442e9433d9eb563e6097176f37c7729122d5323fbbeb4d559.png'
  },
  {
    id: 'customer-service',
    title: 'Customer Service',
    description: 'Inquire about products, services, returns, and troubleshooting assistance.',
    icon: UserCircle,
    path: '/customer-service',
    color: '#8A9A86',
    avatar: 'https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/8f900730b6f0bdc3b684ee4b5fabfa41ba5b5402cabb1ecc7d5370b8fd439d65.png'
  }
];

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen" style={{ background: '#F9F8F5' }}>
      {/* Header */}
      <header className="backdrop-blur-xl bg-white/70 border-b border-white/40 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl sm:text-4xl font-heading font-light tracking-tight" style={{ color: '#1A1D1C' }} data-testid="dashboard-title">
            Multi Task Chatbox
          </h1>
          <p className="text-base leading-relaxed mt-2" style={{ color: '#5C6661' }}>
            Choose an agent to get started
          </p>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div 
          className="rounded-2xl p-12 mb-12" 
          style={{ 
            backgroundImage: `url('https://static.prod-images.emergentagent.com/jobs/85c8ae67-c17b-4832-a183-28703bc48d80/images/79e52084f49bee922cadcd256d768898fac5fc2a4c86fa6fd168837afc5ffb8d.png')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
          data-testid="hero-section"
        >
          <div className="backdrop-blur-sm bg-white/80 rounded-2xl p-8 max-w-2xl">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl tracking-tight font-medium mb-4" style={{ color: '#1A1D1C' }}>
              Your Health & Service Hub
            </h2>
            <p className="text-lg leading-relaxed" style={{ color: '#5C6661' }}>
              Access AI-powered healthcare advice, submit applications, get support, and manage appointments all in one place.
            </p>
          </div>
        </div>

        {/* Agent Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => {
            const IconComponent = agent.icon;
            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                whileHover={{ y: -4 }}
                className="bg-white rounded-2xl p-6 border cursor-pointer"
                style={{ borderColor: '#E8E5DD' }}
                onClick={() => navigate(agent.path)}
                data-testid={`agent-card-${agent.id}`}
              >
                <div className="flex items-start gap-4 mb-4">
                  <div 
                    className="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0"
                    style={{ backgroundColor: `${agent.color}15` }}
                  >
                    <IconComponent size={24} weight="duotone" style={{ color: agent.color }} />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl sm:text-2xl tracking-tight font-medium mb-2" style={{ color: '#1A1D1C' }}>
                      {agent.title}
                    </h3>
                  </div>
                </div>
                <p className="text-sm" style={{ color: '#5C6661' }}>
                  {agent.description}
                </p>
                <button
                  className="mt-6 px-8 py-3 rounded-full text-white font-medium transition-all duration-300 w-full hover:shadow-lg"
                  style={{ 
                    backgroundColor: agent.color,
                    transform: 'scale(1)'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(0.98)'}
                  onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                  data-testid={`agent-btn-${agent.id}`}
                >
                  Get Started
                </button>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;