"""API Service for Gemini-powered backend"""
import axios, { AxiosInstance } from 'axios';
import { ChatMessage, ChatResponse, UploadResponse, HealthResponse } from '../types/api';

class GeminiApiService {
  private api: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Send a chat message to the AI
   */
  async sendMessage(message: string, sessionId: string = 'default'): Promise<ChatResponse> {
    const payload: ChatMessage = {
      message,
      session_id: sessionId,
      stream: false,
    };

    const response = await this.api.post<ChatResponse>('/chat/message', payload);
    return response.data;
  }

  /**
   * Send a message with streaming response
   */
  async sendMessageStream(message: string, sessionId: string = 'default'): Promise<ReadableStream> {
    const payload: ChatMessage = {
      message,
      session_id: sessionId,
      stream: true,
    };

    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.body) {
      throw new Error('No response body');
    }

    return response.body;
  }

  /**
   * Upload CSV file for knowledge base
   */
  async uploadCSV(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.api.post<UploadResponse>('/upload/csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Get conversation history
   */
  async getHistory(sessionId: string = 'default') {
    const response = await this.api.get(`/chat/history/${sessionId}`);
    return response.data;
  }

  /**
   * Clear conversation history
   */
  async clearHistory(sessionId: string = 'default') {
    const response = await this.api.delete(`/chat/history/${sessionId}`);
    return response.data;
  }

  /**
   * Get knowledge base stats
   */
  async getKnowledgeStats() {
    const response = await this.api.get('/upload/stats');
    return response.data;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await this.api.get<HealthResponse>('/health');
    return response.data;
  }
}

export const apiService = new GeminiApiService();
export default GeminiApiService;
