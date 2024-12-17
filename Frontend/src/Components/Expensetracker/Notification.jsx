
import React from 'react';

const Notification = ({ type, message }) => {
  const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
  return (
    <div className={`p-4 rounded shadow text-white ${bgColor}`}>
      {message}
    </div>
  );
};

export default Notification;
