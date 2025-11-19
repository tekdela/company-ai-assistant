import React, { useState, useEffect, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

const API_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentTime, setCurrentTime] = useState('');
  const [uploadStatus, setUploadStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: Date.now().toString(),
      text: `Xin chào! 👋 Tôi là Trợ lý AI nội bộ của công ty.

Tôi có thể giúp bạn:
📋 Tìm kiếm thông tin từ tài liệu nội bộ
⏰ Xem giờ hiện tại (VN, Nhật, Hàn, Mỹ)
🔄 Dịch Việt-Nhật cho thuật ngữ kỹ thuật

Hãy thử hỏi tôi bất cứ điều gì!`,
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString('vi-VN')
    };
    setMessages([welcomeMessage]);
  }, []);

  // Update current time
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('vi-VN'));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: text,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString('vi-VN')
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Call API
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // Add bot response
      setTimeout(() => {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          sender: 'bot',
          timestamp: data.timestamp || new Date().toLocaleTimeString('vi-VN')
        };
        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
      }, 500);

    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '❌ Xin lỗi, có lỗi xảy ra khi kết nối với server. Vui lòng thử lại.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString('vi-VN')
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    }
  };

  const handleSend = () => {
    sendMessage(inputValue);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    'Bây giờ mấy giờ?',
    'Giờ ở Nhật Bản là mấy giờ?',
    'Dịch sang tiếng Nhật "cảm ơn"',
  ];

  // File upload handling
  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploadStatus(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/upload-knowledge`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setUploadStatus({
          type: 'success',
          message: data.message
        });
        
        // Add system message
        const systemMessage: Message = {
          id: Date.now().toString(),
          text: `✅ ${data.message}\n\nBạn có thể bắt đầu hỏi về thông tin trong file này.`,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString('vi-VN')
        };
        setMessages(prev => [...prev, systemMessage]);
      } else {
        setUploadStatus({
          type: 'error',
          message: data.detail || 'Lỗi upload file'
        });
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: 'Không thể kết nối với server'
      });
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  });

  return (
    <div className="App">
      <div className="chat-container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="logo-section">
            <h1>🤖 Trợ lý AI</h1>
            <p>Công ty nội bộ</p>
          </div>

          {/* File Upload */}
          <div className="upload-section">
            <h3>📁 Upload Tài liệu</h3>
            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
              <input {...getInputProps()} />
              <div className="dropzone-content">
                <div className="dropzone-icon">📤</div>
                <div>
                  {isDragActive ? (
                    <p>Thả file vào đây...</p>
                  ) : (
                    <>
                      <p><strong>Kéo thả file</strong></p>
                      <p className="dropzone-text">hoặc click để chọn</p>
                      <p className="dropzone-text">.csv, .txt</p>
                    </>
                  )}
                </div>
              </div>
            </div>
            {uploadStatus && (
              <div className={`upload-status ${uploadStatus.type}`}>
                {uploadStatus.message}
              </div>
            )}
          </div>

          {/* Quick Questions */}
          <div className="quick-questions">
            <h3>💡 Câu hỏi nhanh</h3>
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                className="quick-question-btn"
                onClick={() => sendMessage(question)}
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        {/* Chat Area */}
        <div className="chat-area">
          <div className="chat-header">
            <h2>💬 Trò chuyện</h2>
            <div className="current-time">
              <span>⏰</span>
              <span>{currentTime}</span>
            </div>
          </div>

          <div className="messages-container">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.sender}`}>
                <div className="message-avatar">
                  {message.sender === 'bot' ? '🤖' : '👤'}
                </div>
                <div className="message-content">
                  <div className="message-bubble">
                    {message.text}
                  </div>
                  <div className="message-timestamp">
                    {message.timestamp}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="message bot">
                <div className="message-avatar">🤖</div>
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <div className="input-wrapper">
              <input
                type="text"
                placeholder="Nhập câu hỏi của bạn..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
              />
              <button
                className="send-button"
                onClick={handleSend}
                disabled={!inputValue.trim() || isTyping}
              >
                ➤
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
