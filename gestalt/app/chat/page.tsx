// components/ChatInterface.tsx
'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

type Message = {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  isComplete?: boolean;
};

export default function ChatInterface({ threadId = "123" }: { threadId?: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Handle WebSocket messages
  const handleMessage = useCallback((data: string, sender: 'user' | 'ai', isComplete = false) => {
    setMessages(prev => {
      // For AI messages, append to the last AI message if it exists and isn't complete
      if (sender === 'ai' && prev.length > 0 && prev[prev.length - 1].sender === 'ai' && !prev[prev.length - 1].isComplete) {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: updated[updated.length - 1].content + data,
          timestamp: new Date(),
          isComplete
        };
        return updated;
      }
      
      // Otherwise add new message
      return [
        ...prev,
        {
          id: Date.now().toString(),
          content: data,
          sender,
          timestamp: new Date(),
          isComplete
        }
      ];
    });

    // If the message is complete, stop loading
    if (isComplete) {
      setIsLoading(false);
    }
  }, []);

  // Initialize WebSocket connection
  useEffect(() => {
    const wsUrl = `ws://localhost:8000/ws/${threadId}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      setIsLoading(false);
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // Handle both string messages and structured messages with completion flag
        if (typeof data === 'object' && 'content' in data) {
          handleMessage(data.content, 'ai', data.isComplete);
        } else {
          handleMessage(event.data, 'ai');
        }
      } catch {
        // Fallback for plain text messages
        handleMessage(event.data, 'ai');
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
      setIsLoading(false);
    };

    wsRef.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
      setIsLoading(false);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [threadId, handleMessage]);

  // Auto-scroll and focus management
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    if (messages.length === 0) inputRef.current?.focus();
  }, [messages]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && wsRef.current?.readyState === WebSocket.OPEN && !isLoading) {
      // Add user message immediately
      handleMessage(inputValue, 'user', true);
      
      // Send to WebSocket
      wsRef.current.send(inputValue);
      setIsLoading(true);
      setInputValue('');
    }
  };

  return (
    <div className="container-fluid d-flex flex-column vh-100 p-3" style={{ maxWidth: '800px' }}>
      <h1 className="text-center mb-3">AI Chat Assistant</h1>
      
      {/* Connection status */}
      <div className={`alert alert-${isConnected ? 'success' : 'danger'} py-1 mb-2`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>
      
      {/* Chat messages */}
      <div className="flex-grow-1 border rounded p-3 mb-3 overflow-auto bg-light">
        {messages.length === 0 ? (
          <div className="text-muted text-center py-5">
            Start a conversation with the AI
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`d-flex mb-3 ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
            >
              <div
                className={`p-3 rounded ${msg.sender === 'user' ? 'bg-primary text-white' : 'bg-white border'} shadow-sm`}
                style={{ maxWidth: '80%' }}
              >
                <div className="whitespace-pre-wrap">
                  {msg.content.split('\n').map((line, i) => (
                    <p key={i} className={i > 0 ? 'mt-2 mb-0' : 'mb-0'}>{line}</p>
                  ))}
                </div>
                <div className="text-end text-muted small mt-1">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input form */}
      <form onSubmit={sendMessage} className="d-flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          className="form-control flex-grow-1"
          placeholder="Type your message..."
          disabled={!isConnected || isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary d-flex align-items-center"
          disabled={!inputValue.trim() || !isConnected || isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Sending...
            </>
          ) : 'Send'}
        </button>
      </form>
    </div>
  );
}