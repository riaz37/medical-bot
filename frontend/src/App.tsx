/**
 * Main App component
 */
import React, { useEffect, useRef } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { useMedicalBot } from '@/hooks/useMedicalBot';
import { Header, ChatMessage, ChatInput, EmptyState } from '@/components';
import { cn } from '@/utils/cn';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const AppContent: React.FC = () => {
  const {
    messages,
    isLoading,
    error,
    isHealthy,
    isHealthLoading,
    submitQuery,
    clearMessages,
  } = useMedicalBot();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmitQuery = (query: string) => {
    submitQuery(query, true);
  };

  const handleSampleQuestionClick = (question: string) => {
    submitQuery(question, true);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <Header
        isHealthy={isHealthy}
        isHealthLoading={isHealthLoading}
        messageCount={messages.length}
        onClearMessages={clearMessages}
      />

      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <EmptyState
              onQuestionClick={handleSampleQuestionClick}
              isLoading={isLoading}
            />
          ) : (
            <div className="max-w-4xl mx-auto">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              
              {/* Loading indicator */}
              {isLoading && (
                <div className="flex justify-start p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-medical-500 rounded-full flex items-center justify-center">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    </div>
                    <div className="bg-gray-100 rounded-lg px-4 py-3">
                      <div className="flex items-center gap-2 text-gray-600">
                        <div className="flex gap-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        </div>
                        <span className="text-sm">Thinking...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Error message */}
              {error && (
                <div className="p-4">
                  <div className="max-w-3xl bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">
                      <strong>Error:</strong> {error.message}
                    </p>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <ChatInput
          onSubmit={handleSubmitQuery}
          isLoading={isLoading}
          disabled={!isHealthy}
        />
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
};

export default App;
