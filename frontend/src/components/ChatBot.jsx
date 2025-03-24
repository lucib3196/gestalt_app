import React, { useState } from 'react';
import api from '../api.js';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Append the user's message to the chat log
    const userMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Send user message to the backend /chat endpoint
      const response = await api.post('/chat', {
        messages: [input],
        thread_id: "default"
      });

      // Append the chatbot's reply to the chat log
      const botMessage = { role: "bot", content: response.data };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message", error);
      // Optionally show error feedback in the UI
    }

    setInput("");
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2>ChatBot</h2>
      <div
        style={{
          border: '1px solid #ccc',
          padding: '10px',
          height: '300px',
          overflowY: 'scroll',
          marginBottom: '10px'
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              margin: "5px 0"
            }}
          >
            <strong>{msg.role === "user" ? "You:" : "Bot:"}</strong> {msg.content}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ width: "80%", padding: "8px" }}
        />
        <button type="submit" style={{ width: "18%", padding: "8px" }}>Send</button>
      </form>
    </div>
  );
};

export default ChatBot;
