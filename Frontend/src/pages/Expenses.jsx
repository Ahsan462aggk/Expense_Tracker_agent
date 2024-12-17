// src/pages/Expenses.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import ExpenseList from '../Components/Expensetracker/ExpenseList';

const Expenses = () => {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold text-secondary">Your Expenses</h1>
        <Link to="/add-expense" className="bg-primary text-white px-4 py-2 rounded hover:bg-secondary transition-colors">
          Add Expense
        </Link>
      </div>
      <ExpenseList />
    </div>
  );
};

export default Expenses;
