import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/gemini-api';
import { ConversationMessage } from '../types/api';

export const GeminiChat: React.FC = () => {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState('default');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ConversationMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await apiService.sendMessage(inputMessage, sessionId);
      
      const assistantMessage: ConversationMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: response.metadata.timestamp,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: ConversationMessage = {
        role: 'assistant',
        content: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.',
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus('');
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setUploadStatus('Đang tải lên...');

    try {
      const response = await apiService.uploadCSV(selectedFile);
      
      if (response.success) {
        setUploadStatus(`✅ ${response.message} - ${response.stats.rows} dòng, ${response.stats.columns} cột`);
        setSelectedFile(null);
        
        // Add system message
        const systemMessage: ConversationMessage = {
          role: 'assistant',
          content: `Đã tải lên file ${response.filename} thành công. Bây giờ bạn có thể hỏi tôi về dữ liệu trong file này.`,
          timestamp: new Date().toISOString(),
        };
        
        setMessages(prev => [...prev, systemMessage]);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('❌ Lỗi khi tải file. Vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🤖 Trợ lý AI Công ty</h1>
        <p>Powered by Google Gemini AI</p>
      </div>

      {uploadStatus && (
        <div className={uploadStatus.includes('✅') ? 'success-message' : 'error-message'}>
          {uploadStatus}
        </div>
      )}

      <div className="messages-container">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <p>👋 Xin chào! Tôi là trợ lý AI của công ty.</p>
            <p>Hãy hỏi tôi bất kỳ câu hỏi nào hoặc tải lên file CSV để phân tích.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div>
              <div className="message-content">
                {msg.content}
              </div>
              <div className="message-timestamp">
                {new Date(msg.timestamp).toLocaleTimeString('vi-VN')}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content loading">
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="upload-area">
        <input
          type="file"
          id="file-upload"
          className="file-input"
          accept=".csv"
          onChange={handleFileSelect}
        />
        <label htmlFor="file-upload" className="upload-label">
          📁 Chọn file CSV
        </label>
        
        {selectedFile && (
          <>
            <div className="file-name">
              {selectedFile.name}
            </div>
            <button
              className="upload-button"
              onClick={handleFileUpload}
              disabled={isLoading}
            >
              Tải lên
            </button>
          </>
        )}
      </div>

      <div className="input-container">
        <textarea
          className="message-input"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Nhập tin nhắn của bạn..."
          rows={1}
          disabled={isLoading}
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={isLoading || !inputMessage.trim()}
        >
          Gửi
        </button>
      </div>
    </div>
  );
};

export default GeminiChat;
