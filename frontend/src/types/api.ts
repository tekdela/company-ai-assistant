// TypeScript type definitions

export interface ChatMessage {
  message: string;
  session_id?: string;
  stream?: boolean;
}

export interface ChatResponse {
  response: string;
  metadata: {
    intent: string;
    confidence?: number;
    timestamp: string;
    [key: string]: any;
  };
  session_id: string;
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  filename: string;
  stats: {
    loaded: boolean;
    rows?: number;
    columns?: number;
    column_names?: string[];
  };
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  services: {
    [key: string]: boolean;
  };
}
