import React from 'react';
import { Link } from 'react-router-dom';
import { 
  CreditCard, 
  BarChart2, 
  PiggyBank 
} from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-purple-600 flex flex-col">
      {/* Main Content */}
      <div className="flex-grow flex flex-col items-center justify-center px-4 text-center">
        {/* Hero Section */}
        <div className="max-w-4xl">
          <h1 className="
            text-4xl md:text-6xl font-extrabold 
            text-white mb-6 tracking-tight 
            drop-shadow-lg
          ">
            ExpenseTracker
          </h1>
          
          <p className="
            text-xl md:text-2xl text-white/90 
            mb-8 max-w-2xl mx-auto
            leading-relaxed
          ">
            Simplify your financial management with intelligent expense tracking 
            and insightful analytics
          </p>
          
          {/* Call to Action Buttons */}
          <div className="flex justify-center space-x-4">
            <Link 
              to="/login" 
              className="
                flex items-center space-x-2
                bg-white/20 text-white 
                px-6 py-3 rounded-lg 
                hover:bg-white/30 
                transition-all duration-300 
                focus:outline-none 
                focus:ring-2 focus:ring-white/50
              "
            >
              <span>Login</span>
            </Link>
            
            <Link 
              to="/register" 
              className="
                flex items-center space-x-2
                bg-white/10 text-white 
                px-6 py-3 rounded-lg 
                hover:bg-white/20 
                transition-all duration-300 
                focus:outline-none 
                focus:ring-2 focus:ring-white/50
              "
            >
              <span>Register</span>
            </Link>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="
          mt-16 grid grid-cols-1 md:grid-cols-3 
          gap-6 max-w-4xl w-full
          text-white
        ">
          <div className="
            bg-white/10 rounded-lg p-6 
            flex flex-col items-center 
            text-center hover:bg-white/20 
            transition-all duration-300
          ">
            <CreditCard size={40} className="mb-4" />
            <h3 className="text-xl font-semibold mb-2">
              Track Expenses
            </h3>
            <p className="text-white/80">
              Effortlessly log and categorize your daily expenses
            </p>
          </div>

          <div className="
            bg-white/10 rounded-lg p-6 
            flex flex-col items-center 
            text-center hover:bg-white/20 
            transition-all duration-300
          ">
            <BarChart2 size={40} className="mb-4" />
            <h3 className="text-xl font-semibold mb-2">
              Detailed Analytics
            </h3>
            <p className="text-white/80">
              Gain insights with comprehensive financial reports
            </p>
          </div>

          <div className="
            bg-white/10 rounded-lg p-6 
            flex flex-col items-center 
            text-center hover:bg-white/20 
            transition-all duration-300
          ">
            <PiggyBank size={40} className="mb-4" />
            <h3 className="text-xl font-semibold mb-2">
              Smart Savings
            </h3>
            <p className="text-white/80">
              Set goals and track your progress towards financial freedom
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;