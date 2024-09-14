// src/App.js
import React from 'react';
import Upload from './components/Upload';
import AskQuestion from './components/AskQuestion';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-4">Contract Analysis Chatbot</h1>
      <Upload />
      <AskQuestion />
    </div>
  );
};

export default App;
