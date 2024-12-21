import React, { useState, useRef, useEffect } from 'react';
import { Sparkles, Bot } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import ExpenseList from './ExpenseList';

const ChatBox = () => {
  const [message, setMessage] = useState('');
  const [displayedResponse, setDisplayedResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);
  const typingTimerRef = useRef(null);

  // Typing effect function
  const typeResponse = (text) => {
    let currentIndex = 0;
    if (typingTimerRef.current) {
      clearInterval(typingTimerRef.current);
    }
    typingTimerRef.current = setInterval(() => {
      if (currentIndex <= text.length) {
        setDisplayedResponse(text.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(typingTimerRef.current);
        const agentMessageObj = { type: 'agent', text };
        setChatHistory((prev) => [...prev, agentMessageObj]);
        setDisplayedResponse('');
      }
    }, 20);
  };

  const handleInteract = async (e) => {
    e.preventDefault();
    if (message.trim() === '') return;

    const userMessage = { type: 'user', text: message };
    setChatHistory((prev) => [...prev, userMessage]);

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8090/agents/query', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: message }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get response from AI Agent.');
      }

      const data = await response.json();
      typeResponse(data.response);
    } catch (err) {
      console.error('AI Agent interaction failed:', err);
      const errorMsg = err.message || 'Failed to get response from AI Agent.';
      setError(errorMsg);
      const errorMessageObj = { type: 'error', text: errorMsg };
      setChatHistory((prev) => [...prev, errorMessageObj]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, displayedResponse]);

  // Clean up typing timer on unmount
  useEffect(() => {
    return () => {
      if (typingTimerRef.current) {
        clearInterval(typingTimerRef.current);
      }
    };
  }, []);

  const renderChatMessage = (msg, index) => {
    switch (msg.type) {
      case 'user':
        return (
          <div key={index} className="flex justify-end mb-3">
            <div className="bg-indigo-100 text-indigo-800 px-3 py-2 rounded-lg max-w-[80%]">
              {msg.text}
            </div>
          </div>
        );
      case 'agent':
        return (
          <div key={index} className="flex mb-3">
            <div className="bg-purple-100 text-purple-800 px-3 py-2 rounded-lg max-w-[80%]">
              {msg.text}
            </div>
          </div>
        );
      case 'error':
        return (
          <div key={index} className="flex mb-3">
            <div className="bg-red-100 text-red-800 px-3 py-2 rounded-lg max-w-[80%]">
              {msg.text}
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="mt-16 p-4 md:flex md:space-x-4" style={{ maxHeight: '600px' }}>
      {/* Left Column: ChatBox */}
      <div 
        className="w-full md:w-2/3 bg-white shadow-xl rounded-xl overflow-hidden mb-4 md:mb-0 flex flex-col" 
        style={{ maxHeight: '600px' }}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-4 flex items-center">
          <Bot className="mr-2 text-white" size={24} />
          <h2 className="text-xl font-bold text-white">AI Agent</h2>
        </div>

        {/* Chat Area */}
        <div className="p-4 space-y-3 flex flex-col h-full">
          <div className="flex-grow overflow-y-auto border border-gray-200 rounded-lg p-3">
            {chatHistory.length === 0 && !loading && !displayedResponse ? (
              <div className="text-center text-gray-500 flex flex-col items-center justify-center h-full">
                <Sparkles className="text-indigo-500 mb-2" size={32} />
                <p>Ask me anything about your expenses!</p>
              </div>
            ) : (
              <div>
                {chatHistory.map(renderChatMessage)}
                {loading && (
                  <div className="flex mb-3">
                    <div className="bg-purple-100 text-purple-800 px-3 py-2 rounded-lg">
                      <LoadingSpinner size="sm" />
                    </div>
                  </div>
                )}
                {displayedResponse && (
                  <div className="flex mb-3">
                    <div className="bg-purple-100 text-purple-800 px-3 py-2 rounded-lg max-w-[80%]">
                      {displayedResponse}
                      <span className="animate-pulse text-purple-500">|</span>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <form onSubmit={handleInteract} className="flex space-x-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all duration-300"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white 
                p-2 rounded-lg hover:from-indigo-700 hover:to-purple-700 
                transition-all duration-300 flex items-center justify-center 
                disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <LoadingSpinner size="sm" /> : 'Send'}
            </button>
          </form>

          {/* Error Handling */}
          {error && (
            <div
              className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded-lg"
              role="alert"
            >
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Right Column: Expense List */}
      <div 
        className="w-full md:w-1/2 flex flex-col bg-white shadow-xl rounded-xl overflow-hidden border border-gray-100" 
        style={{ maxHeight: '600px' }}
      >
        <div className="bg-gray-100 p-4 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">Your Expenses</h3>
          <p className="text-sm text-gray-500">View, edit, and delete your expenses</p>
        </div>
        <div className="flex-grow overflow-y-auto p-4">
          <ExpenseList />
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
