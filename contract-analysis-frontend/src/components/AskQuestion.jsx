import React, { useState } from 'react';
import axios from 'axios';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(''); // State for storing the answer
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Handle question input change
  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleAskQuestion = async () => {
    setLoading(true);
    setError('');
    setAnswer('');  // Clear the previous answer
    try {
      // Add the correct backend URL (check if it's localhost or 127.0.0.1)
      const response = await axios.post('http://127.0.0.1:5000/ask', { question }, {
        headers: { 'Content-Type': 'application/json' }
      });
      
      // Log the full response to see what you get from the backend
      console.log('Response from server:', response.data); 
  
      // Check if the response contains the 'answer' field and set it
      if (response.data.answer) {
        setAnswer(response.data.answer);
      } else {
        setError('No answer received from the server');
      }
    } catch (error) {
      console.error('Error asking question:', error);
      setError('Error asking question.');
    } finally {
      setLoading(false);
    }
  };
  
  

  return (
    <div className="p-4 max-w-lg mx-auto">
      <label htmlFor="questionInput">Question:</label>
      <input 
        id="questionInput"  // Unique ID
        name="question"      // Name attribute for autofill and accessibility
        type="text" 
        value={question} 
        onChange={handleQuestionChange} 
        className="border rounded p-2 w-full mb-2"
        placeholder="Ask a question..."
        autoComplete="off"  // Disable autofill for this field if needed
      />

      <button 
        onClick={handleAskQuestion} 
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        disabled={loading}
      >
        {loading ? 'Asking...' : 'Ask'}
      </button>

      {/* Display error if present */}
      {error && <p className="mt-2 text-red-500">{error}</p>}

      {/* Separate Textarea for the Answer */}
      <div className="mt-4">
        <label className="block mb-1 font-semibold">Answer:</label>
        <textarea
          value={answer} // Set the value of the textarea to the answer state
          readOnly // Make it read-only
          className="w-full p-2 border rounded h-32"
          placeholder="The answer will appear here..."
        />
      </div>
    </div>
  );
};

export default AskQuestion;
