import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CalendarDays, 
  FileText, 
  DollarSign, 
  Tag, 
  Save 
} from 'lucide-react';

const ExpenseForm = ({ initialData = {}, isEdit = false }) => {
  const [description, setDescription] = useState(initialData.description || '');
  const [amount, setAmount] = useState(initialData.amount || '');
  const [category, setCategory] = useState(initialData.category || '');
  const [date, setDate] = useState(initialData.date ? initialData.date.substring(0,10) : '');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  console.log("initial",initialData)


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Retrieve user_id from local storage
    const userId = localStorage.getItem('user_id');
    
    const expenseData = {
      description,
      amount: parseFloat(amount),
      category,
      date: date || "",
      user_id: userId ? parseInt(userId, 10) : 0,
    };

    try {
      const response = await fetch(
        isEdit 
          ? `http://localhost:8090/expenses/${initialData.id}`
          : 'http://localhost:8090/expenses/',
        {
          method: isEdit ? 'PUT' : 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(expenseData),
          credentials: 'include',
        }
      );

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      navigate('/expenses');
    } catch (err) {
      console.error('Failed to submit expense:', err);
      setError('Failed to submit expense. Please try again.');
    }
  };

  const inputClasses = "w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-300 text-base";
  const labelClasses = "block text-sm font-medium text-gray-700 mb-2 flex items-center";

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white shadow-2xl rounded-2xl overflow-hidden">
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-8">
          <h2 className="text-4xl font-bold text-white text-center">
            {isEdit ? 'Edit Expense' : 'Add New Expense'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-10 space-y-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-6">
            {/* Description Input */}
            <div>
              <label className={labelClasses}>
                <FileText className="mr-2 text-indigo-500" size={20} />
                Description
              </label>
              <div className="relative">
                <input 
                  type="text" 
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className={inputClasses}
                  placeholder="Enter expense description"
                />
              </div>
            </div>

            {/* Amount Input */}
            <div>
              <label className={labelClasses}>
                <DollarSign className="mr-2 text-indigo-500" size={20} />
                Amount
              </label>
              <div className="relative">
                <input 
                  type="number" 
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  required
                  step="0.01"
                  className={inputClasses}
                  placeholder="0.00"
                />
              </div>
            </div>

            {/* Category Input */}
            <div>
              <label className={labelClasses}>
                <Tag className="mr-2 text-indigo-500" size={20} />
                Category
              </label>
              <div className="relative">
                <input 
                  type="text" 
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  required
                  className={inputClasses}
                  placeholder="Expense category"
                />
              </div>
            </div>

            {/* Date Input */}
            <div>
              <label className={labelClasses}>
                <CalendarDays className="mr-2 text-indigo-500" size={20} />
                Date
              </label>
              <div className="relative">
                <input 
                  type="date" 
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className={inputClasses}
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button 
            type="submit" 
            className="w-full mt-6 flex items-center justify-center py-4 px-4 
              bg-gradient-to-r from-indigo-600 to-purple-600 
              text-white text-lg font-semibold rounded-lg 
              hover:from-indigo-700 hover:to-purple-700 
              focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 
              transition-all duration-300 transform hover:scale-105"
          >
            <Save className="mr-2" size={24} />
            {isEdit ? 'Update Expense' : 'Add Expense'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ExpenseForm;
