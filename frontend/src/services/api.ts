/**
 * API service for communicating with the medical bot backend
 */
import axios, { AxiosResponse } from 'axios';
import type {
  QueryRequest,
  QueryResponse,
  HealthCheckResponse,
  SourceDocument,
  DocumentUploadResponse,
  ApiError,
} from '@/types/api';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const apiError: ApiError = {
      message: error.response?.data?.message || error.message || 'An error occurred',
      status: error.response?.status,
      details: error.response?.data?.details,
    };
    return Promise.reject(apiError);
  }
);

/**
 * Medical Bot API Service
 */
export class MedicalBotAPI {
  /**
   * Submit a medical query to the bot
   */
  static async query(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response: AxiosResponse<QueryResponse> = await api.post('/query', request);
      return response.data;
    } catch (error) {
      throw error as ApiError;
    }
  }

  /**
   * Search for similar documents
   */
  static async searchDocuments(query: string, limit: number = 4): Promise<SourceDocument[]> {
    try {
      const response: AxiosResponse<SourceDocument[]> = await api.get('/search', {
        params: { query, limit },
      });
      return response.data;
    } catch (error) {
      throw error as ApiError;
    }
  }

  /**
   * Upload a document file
   */
  static async uploadDocument(file: File): Promise<DocumentUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response: AxiosResponse<DocumentUploadResponse> = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error as ApiError;
    }
  }

  /**
   * Check API health status
   */
  static async healthCheck(): Promise<HealthCheckResponse> {
    try {
      const response: AxiosResponse<HealthCheckResponse> = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error as ApiError;
    }
  }
}

export default MedicalBotAPI;
