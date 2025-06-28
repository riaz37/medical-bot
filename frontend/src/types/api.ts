/**
 * TypeScript types for API requests and responses
 */

export interface QueryRequest {
  query: string;
  include_sources?: boolean;
  max_sources?: number;
}

export interface SourceDocument {
  content: string;
  metadata: Record<string, any>;
  relevance_score?: number;
}

export interface QueryResponse {
  answer: string;
  sources?: SourceDocument[];
  query: string;
  processing_time: number;
  model_used: string;
}

export interface HealthCheckResponse {
  status: string;
  version: string;
  timestamp: string;
  services: Record<string, string>;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
}

export interface DocumentUploadResponse {
  message: string;
  document_id: string;
  chunks_created: number;
  processing_time: number;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}
