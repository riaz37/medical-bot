/**
 * Custom hook for medical bot interactions
 */
import { useState, useCallback } from 'react';
import { useMutation, useQuery } from 'react-query';
import MedicalBotAPI from '@/services/api';
import type { QueryRequest, ChatMessage, ApiError } from '@/types';

export const useMedicalBot = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Health check query
  const {
    data: healthStatus,
    isLoading: isHealthLoading,
    error: healthError,
  } = useQuery('health', MedicalBotAPI.healthCheck, {
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
  });

  // Query mutation
  const queryMutation = useMutation(MedicalBotAPI.query, {
    onSuccess: (data, variables) => {
      // Add user message
      const userMessage: ChatMessage = {
        id: `user-${Date.now()}`,
        type: 'user',
        content: variables.query,
        timestamp: new Date(),
      };

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        type: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        sources: data.sources,
        processing_time: data.processing_time,
      };

      setMessages(prev => [...prev, userMessage, assistantMessage]);
    },
    onError: (error: ApiError) => {
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    },
  });

  // Document upload mutation
  const uploadMutation = useMutation(MedicalBotAPI.uploadDocument);

  // Submit query function
  const submitQuery = useCallback(
    (query: string, includeSources: boolean = true) => {
      const request: QueryRequest = {
        query: query.trim(),
        include_sources: includeSources,
        max_sources: 3,
      };

      queryMutation.mutate(request);
    },
    [queryMutation]
  );

  // Upload document function
  const uploadDocument = useCallback(
    (file: File) => {
      return uploadMutation.mutateAsync(file);
    },
    [uploadMutation]
  );

  // Clear messages function
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    // State
    messages,
    isLoading: queryMutation.isLoading,
    isUploading: uploadMutation.isLoading,
    error: queryMutation.error as ApiError | null,
    uploadError: uploadMutation.error as ApiError | null,
    healthStatus,
    isHealthLoading,
    healthError: healthError as ApiError | null,

    // Actions
    submitQuery,
    uploadDocument,
    clearMessages,

    // Status
    isHealthy: healthStatus?.status === 'healthy',
  };
};
