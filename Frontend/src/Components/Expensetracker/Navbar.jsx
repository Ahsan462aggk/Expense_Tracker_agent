import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  Home, 
  CreditCard, 
  Bot, 
  LogOut, 
  Menu, 
  X 
} from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      // Assuming you have an API method for logout
      // await api.post('/users/logout');
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const navItems = [
    { 
      name: 'Dashboard', 
      path: '/dashboard', 
      icon: Home 
    },
    { 
      name: 'Expenses', 
      path: '/expenses', 
      icon: CreditCard 
    },
    { 
      name: 'AI Agent', 
      path: '/agent', 
      icon: Bot 
    }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link 
            to="/dashboard" 
            className="flex items-center space-x-2 text-white hover:text-gray-200 transition-colors duration-300"
          >
            <span className="text-xl font-bold tracking-wider">
              ExpenseTracker
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium
                  transition-all duration-300 ease-in-out
                  ${isActive(item.path) 
                    ? 'bg-white/20 text-white' 
                    : 'text-white/80 hover:bg-white/10 hover:text-white'}
                `}
              >
                <item.icon size={18} />
                <span>{item.name}</span>
              </Link>
            ))}

            <button
              onClick={handleLogout}
              className="
                flex items-center space-x-2 px-3 py-2 
                bg-red-500/20 hover:bg-red-500/30 
                text-white rounded-md 
                transition-all duration-300 ease-in-out
                focus:outline-none focus:ring-2 focus:ring-red-400
              "
            >
              <LogOut size={18} />
              <span>Logout</span>
            </button>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-white hover:text-gray-200 focus:outline-none"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-indigo-700 absolute top-16 left-0 right-0 shadow-lg">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMenuOpen(false)}
                className={`
                  flex items-center space-x-3 px-3 py-2 rounded-md
                  ${isActive(item.path) 
                    ? 'bg-white/20 text-white' 
                    : 'text-white/80 hover:bg-white/10 hover:text-white'}
                  block text-base font-medium
                `}
              >
                <item.icon size={20} />
                <span>{item.name}</span>
              </Link>
            ))}
            <button
              onClick={() => {
                handleLogout();
                setIsMenuOpen(false);
              }}
              className="
                w-full text-left flex items-center space-x-3 
                px-3 py-2 rounded-md 
                bg-red-500/20 hover:bg-red-500/30 
                text-white
                transition-all duration-300 ease-in-out
                focus:outline-none focus:ring-2 focus:ring-red-400
              "
            >
              <LogOut size={20} />
              <span>Logout</span>
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;