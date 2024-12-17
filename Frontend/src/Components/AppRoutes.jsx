// src/routes/AppRoutes.jsx
import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './Expensetracker/Navbar';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import Expenses from '../pages/Expenses';
import AddExpense from '../pages/AddExpense';
import AgentInteraction from '../pages/AgentInteraction';
import Footer from './Expensetracker/Footer';

const AppRoutes = () => {
  const location = useLocation();
  const hideNavbarAndFooter = ["/login", "/register","/"].includes(location.pathname);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Conditionally render Navbar */}
      {!hideNavbarAndFooter && <Navbar />}

      {/* Main Content Area */}
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/add-expense" element={<AddExpense />} />
          <Route path="/agent" element={<AgentInteraction />} />
          {/* 404 Page */}
          <Route path="*" element={<div className="text-center mt-10 text-secondary text-2xl">404 - Page Not Found</div>} />
        </Routes>
      </main>

      {/* Conditionally render Footer */}
      {!hideNavbarAndFooter && <Footer />}
    </div>
  );
};

export default AppRoutes;
