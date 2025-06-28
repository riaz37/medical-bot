/**
 * Application header component
 */
import React from 'react';
import { Heart, AlertCircle, CheckCircle, Trash2 } from 'lucide-react';
import { cn } from '@/utils/cn';

interface HeaderProps {
  isHealthy: boolean;
  isHealthLoading: boolean;
  messageCount: number;
  onClearMessages: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  isHealthy,
  isHealthLoading,
  messageCount,
  onClearMessages,
}) => {
  const getHealthStatus = () => {
    if (isHealthLoading) {
      return {
        icon: <div className="w-4 h-4 border-2 border-gray-300 border-t-primary-500 rounded-full animate-spin" />,
        text: 'Checking...',
        color: 'text-gray-500',
      };
    }
    
    if (isHealthy) {
      return {
        icon: <CheckCircle className="w-4 h-4" />,
        text: 'Online',
        color: 'text-green-600',
      };
    }
    
    return {
      icon: <AlertCircle className="w-4 h-4" />,
      text: 'Offline',
      color: 'text-red-600',
    };
  };

  const healthStatus = getHealthStatus();

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Logo and title */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-medical-500 to-medical-600 rounded-lg flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Medical Bot</h1>
            <p className="text-sm text-gray-600">AI-powered medical assistant</p>
          </div>
        </div>

        {/* Status and actions */}
        <div className="flex items-center gap-4">
          {/* Health status */}
          <div className={cn('flex items-center gap-2', healthStatus.color)}>
            {healthStatus.icon}
            <span className="text-sm font-medium">{healthStatus.text}</span>
          </div>

          {/* Message count and clear button */}
          {messageCount > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500">
                {messageCount} message{messageCount !== 1 ? 's' : ''}
              </span>
              <button
                onClick={onClearMessages}
                className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                title="Clear conversation"
              >
                <Trash2 className="w-4 h-4" />
                Clear
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
