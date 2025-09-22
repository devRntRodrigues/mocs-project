import axios, { AxiosResponse } from 'axios';
import {
  APIResponse,
  ListResponse,
  DocumentDetail,
  DocumentSummary,
  DocumentUploadResult,
  RAGQuestionResponse,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 100000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    if (error.message) {
      throw new Error(error.message);
    }
    throw new Error('An unexpected error occurred');
  }
);

class DocumentService {
  async uploadDocument(file: File): Promise<DocumentUploadResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response: AxiosResponse<APIResponse<DocumentUploadResult>> = await apiClient.post(
      '/documents/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data.data;
  }

  async listDocuments(): Promise<DocumentSummary[]> {
    const response: AxiosResponse<ListResponse<DocumentSummary>> = await apiClient.get('/documents/');
    return response.data.data;
  }

  async getDocument(id: number): Promise<DocumentDetail> {
    const response: AxiosResponse<APIResponse<DocumentDetail>> = await apiClient.get(`/documents/${id}`);
    return response.data.data;
  }

  async deleteDocument(id: number): Promise<boolean> {
    const response: AxiosResponse<APIResponse<{ deleted: boolean }>> = await apiClient.delete(`/documents/${id}`);
    return response.data.data.deleted;
  }
}

class RAGService {
  async askDocumentQuestion(documentId: number, question: string, maxChunks: number = 3): Promise<RAGQuestionResponse> {
    const response: AxiosResponse<APIResponse<RAGQuestionResponse>> = await apiClient.post(
      `/documents/${documentId}/question`,
      {
        question,
        max_chunks: maxChunks
      }
    );
    return response.data.data;
  }
}

export const documentService = new DocumentService();
export const ragService = new RAGService();

export default apiClient;


