// src/components/Expenses/ExpenseList.jsx
import React, { useEffect, useState } from 'react';
import LoadingSpinner from './LoadingSpinner';
import ExpenseItem from './ExpenseItem';

const ExpenseList = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchExpenses = async () => {
    try {
      const response = await fetch('http://localhost:8090/expenses/',{
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch expenses');
      }
      const data = await response.json();
      setExpenses(data.reverse());
    } catch (error) {
      console.error('Failed to fetch expenses:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8090/expenses/${id}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to delete expense');
      }
      setExpenses((currentExpenses) => currentExpenses.filter(exp => exp.id !== id));
    } catch (error) {
      console.error('Failed to delete expense:', error);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="mt-4">
      {expenses.length === 0 ? (
        <p className="text-center text-gray-500">No expenses found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {expenses.map(expense => (
            <ExpenseItem key={expense.id} expense={expense} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ExpenseList;
