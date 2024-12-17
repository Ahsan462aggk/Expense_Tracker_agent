import React, { useState } from 'react';
import { 
  Edit2, 
  Trash2, 
  FileText, 
  DollarSign, 
  Tag, 
  Calendar, 
  X 
} from 'lucide-react';

const ExpenseItem = ({ expense, onDelete }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editedExpense, setEditedExpense] = useState({
    description: expense.description,
    amount: expense.amount,
    category: expense.category,
    date: expense.date,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      onDelete(expense.id);
    }
  };

  const handleEditClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditedExpense({
      description: expense.description,
      amount: expense.amount,
      category: expense.category,
      date: expense.date,
    });
    setError(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedExpense((prev) => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    const userId = localStorage.getItem('userId');
    if (!userId) {
      setError('User ID not found. Please log in again.');
      setIsSubmitting(false);
      return;
    }

    const updatedData = {
      description: editedExpense.description,
      amount: editedExpense.amount,
      category: editedExpense.category,
      date: new Date(editedExpense.date).toISOString(),
      user_id: parseInt(userId, 10),
    };

    try {
      const response = await fetch(`http://localhost:8090/expenses/${expense.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
     
        body: JSON.stringify(updatedData),
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to update the expense. Please try again.');
      }

      const updatedExpense = await response.json();
      setIsModalOpen(false);
      window.location.reload()
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Helper function to format the date
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Helper function to format the currency
  const formatCurrency = (amount) => {
    return `$${amount.toFixed(2)}`;
  };

  return (
    <>
      <div className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100 transition-all duration-300 hover:shadow-xl">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <FileText className="text-indigo-500 mr-3" size={24} />
            <h3 className="text-xl font-bold text-gray-800 truncate">
              {expense.description}
            </h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center text-gray-600">
              <DollarSign className="text-purple-500 mr-3" size={20} />
              <span className="font-medium text-lg">
                {formatCurrency(expense.amount)}
              </span>
            </div>

            <div className="flex items-center text-gray-500">
              <Tag className="text-indigo-500 mr-3" size={20} />
              <span>{expense.category}</span>
            </div>

            <div className="flex items-center text-gray-500">
              <Calendar className="text-purple-500 mr-3" size={20} />
              <span>{formatDate(expense.date)}</span>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-200 flex justify-between items-center">
            <button 
              onClick={handleEditClick}
              className="flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
            >
              <Edit2 size={20} className="mr-2" />
              Edit
            </button>
            <button 
              onClick={handleDelete} 
              className="flex items-center text-red-500 hover:text-red-700 transition-colors"
            >
              <Trash2 size={20} className="mr-2" />
              Delete
            </button>
          </div>
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
            <button 
              onClick={handleCloseModal} 
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
            >
              <X size={20} />
            </button>
            <h2 className="text-2xl font-bold mb-4">Edit Expense</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="text-red-500 text-sm">
                  {error}
                </div>
              )}
              <div>
                <label className="block text-gray-700">Description</label>
                <input 
                  type="text" 
                  name="description"
                  value={editedExpense.description}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700">Amount</label>
                <input 
                  type="number" 
                  name="amount"
                  value={editedExpense.amount}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded"
                  step="0.01"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700">Category</label>
                <input 
                  type="text" 
                  name="category"
                  value={editedExpense.category}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700">Date</label>
                <input 
                  type="date" 
                  name="date"
                  value={editedExpense.date.split('T')[0]} // Assuming ISO format
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded"
                  required
                />
              </div>
              <div className="flex justify-end space-x-2">
                <button 
                  type="button" 
                  onClick={handleCloseModal}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Saving...' : 'Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default ExpenseItem;
