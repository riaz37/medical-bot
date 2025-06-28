/**
 * Main types export file
 */

export * from './api';

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: SourceDocument[];
  processing_time?: number;
}

export interface AppState {
  isLoading: boolean;
  error: string | null;
  messages: ChatMessage[];
}

import type { SourceDocument } from './api';
