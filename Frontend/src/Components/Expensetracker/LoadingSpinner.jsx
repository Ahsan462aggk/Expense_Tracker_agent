// src/components/UI/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = ({ size = 'md' }) => {
  const sizes = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-4',
    lg: 'h-12 w-12 border-6',
  };
  return (
    <div className={`flex justify-center items-center`}>
      <div className={`animate-spin rounded-full border-t-2 border-b-2 border-primary ${sizes[size]}`}></div>
    </div>
  );
};

export default LoadingSpinner;
