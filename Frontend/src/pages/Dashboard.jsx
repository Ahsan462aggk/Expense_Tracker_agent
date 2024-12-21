import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  ChartBarIcon, 
  PlusCircleIcon, 
  SparklesIcon 
} from 'lucide-react';
import LoadingSpinner from '../Components/Expensetracker/LoadingSpinner';

// Helper function to format currency
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

const DashboardCard = ({ icon, title, content, action, actionText, actionLink }) => (
  <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl shadow-2xl overflow-hidden transform transition-all  duration-300 hover:scale-105">
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full p-3 text-white">
          {icon}
        </div>
        {action && (
          <Link 
            to={actionLink} 
            className="text-white hover:text-indigo-300 transition-colors"
          >
            {actionText}
          </Link>
        )}
      </div>
      <h2 className="text-xl font-semibold text-white mb-2">{title}</h2>
      <p className="text-3xl font-bold text-white">{content}</p>
    </div>
  </div>
);

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchExpenses = async () => {
    try {
      // Mocked data for simplicity
      const response = {
        data: [
          { id: 1, amount: 1200 },
          { id: 2, amount: 800 },
          { id: 3, amount: 500 },
        ],
      };
      setExpenses(response.data);
    } catch (error) {
      console.error('Failed to fetch expenses:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const totalExpenses = expenses.reduce((acc, exp) => acc + exp.amount, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-600 to-purple-600">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-purple-600 px-4 py-28">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-extrabold text-white mb-12 text-center">
          Expense Dashboard
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <DashboardCard 
            icon={<ChartBarIcon className="w-8 h-8" />}
            title="Total Expenses"
            content={formatCurrency(totalExpenses)}
          />
          
          <DashboardCard 
            icon={<PlusCircleIcon className="w-8 h-8" />}
            title="Manage Expenses"
            action
            actionText="Add Expense"
            actionLink="/add-expense"
          />
          
          <DashboardCard 
            icon={<SparklesIcon className="w-8 h-8" />}
            title="AI Agent"
            action
            actionText="Chat Now"
            actionLink="/agent"
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;