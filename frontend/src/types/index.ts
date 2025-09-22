// Base API Response Structure
export interface APIResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  request_id: string;
  timestamp: string;
}

export interface ListResponse<T> {
  success: boolean;
  data: T[];
  count: number;
  request_id: string;
  timestamp: string;
}

// Document Types
export interface DocumentDetail {
  id: number;
  file_name: string;
  text_content: string;
  created_at: string;
  updated_at?: string;
}

export interface DocumentSummary {
  id: number;
  file_name: string;
  text_length: number;
  created_at: string;
}

export interface DocumentUploadResult {
  id: number;
  file_name: string;
  text_content: string;
  text_length: number;
  processing_time_ms: number;
  created_at: string;
  rag_processing: {
    chunks_created: number;
    rag_processing_time_ms: number;
    status: string;
  };
}

// RAG Types
export interface QuestionRequest {
  question: string;
  document_id?: number;
  max_chunks?: number;
}

export interface SourceChunk {
  content: string;
  document_id: number;
  chunk_id: number;
  source?: string;
}

export interface RAGQuestionResponse {
  question: string;
  answer: string;
  source_chunks: SourceChunk[];
  processing_time_ms: number;
  method: string;
  created_at: string;
}

// Error Types
export interface ErrorResponse {
  detail: string;
}

export interface ApiError {
  message: string;
  status?: number;
}


