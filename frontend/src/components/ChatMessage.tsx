/**
 * Chat message component for displaying user and assistant messages
 */
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Clock, FileText } from 'lucide-react';
import { cn } from '@/utils/cn';
import type { ChatMessage as ChatMessageType } from '@/types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.type === 'user';

  return (
    <div className={cn('flex gap-3 p-4', isUser ? 'justify-end' : 'justify-start')}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-medical-500 rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-white" />
          </div>
        </div>
      )}

      <div className={cn('max-w-3xl', isUser ? 'order-1' : 'order-2')}>
        <div
          className={cn(
            'rounded-lg px-4 py-3',
            isUser
              ? 'bg-primary-500 text-white ml-auto'
              : 'bg-gray-100 text-gray-900 border'
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <ReactMarkdown
              className="prose prose-sm max-w-none"
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
                li: ({ children }) => <li className="mb-1">{children}</li>,
                strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Message metadata */}
        <div className={cn('flex items-center gap-2 mt-1 text-xs text-gray-500', isUser ? 'justify-end' : 'justify-start')}>
          <Clock className="w-3 h-3" />
          <span>{message.timestamp.toLocaleTimeString()}</span>
          {message.processing_time && (
            <span className="text-gray-400">
              • {message.processing_time.toFixed(2)}s
            </span>
          )}
        </div>

        {/* Source documents */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 space-y-2">
            <div className="flex items-center gap-1 text-xs font-medium text-gray-600">
              <FileText className="w-3 h-3" />
              Sources ({message.sources.length})
            </div>
            <div className="space-y-2">
              {message.sources.map((source, index) => (
                <div
                  key={index}
                  className="bg-gray-50 border rounded-md p-3 text-sm"
                >
                  <p className="text-gray-700 mb-2 line-clamp-3">
                    {source.content}
                  </p>
                  {source.metadata.filename && (
                    <div className="text-xs text-gray-500">
                      Source: {source.metadata.filename}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex-shrink-0 order-2">
          <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
        </div>
      )}
    </div>
  );
};
