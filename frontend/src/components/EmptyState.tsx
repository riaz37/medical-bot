/**
 * Empty state component for when no messages are present
 */
import React from 'react';
import { MessageCircle, Lightbulb } from 'lucide-react';

const sampleQuestions = [
  "How is diabetes diagnosed?",
  "What are the side effects of aspirin?",
  "What is the difference between Type 1 and Type 2 diabetes?",
  "How can I prevent heart disease?",
  "What are the warning signs of a stroke?",
];

interface EmptyStateProps {
  onQuestionClick: (question: string) => void;
  isLoading: boolean;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  onQuestionClick,
  isLoading,
}) => {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        {/* Icon */}
        <div className="w-16 h-16 bg-gradient-to-br from-medical-500 to-medical-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <MessageCircle className="w-8 h-8 text-white" />
        </div>

        {/* Title and description */}
        <h2 className="text-2xl font-bold text-gray-900 mb-3">
          Welcome to Medical Bot
        </h2>
        <p className="text-gray-600 mb-8 leading-relaxed">
          I'm an AI-powered medical assistant trained on medical literature. 
          Ask me questions about symptoms, conditions, treatments, or general health information.
        </p>

        {/* Disclaimer */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-8">
          <div className="flex items-start gap-3">
            <Lightbulb className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-left">
              <p className="text-sm font-medium text-amber-800 mb-1">
                Important Disclaimer
              </p>
              <p className="text-sm text-amber-700">
                This AI assistant provides general medical information for educational purposes only. 
                It is not a substitute for professional medical advice, diagnosis, or treatment. 
                Always consult with qualified healthcare providers for medical concerns.
              </p>
            </div>
          </div>
        </div>

        {/* Sample questions */}
        <div className="text-left">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Try asking about:
          </h3>
          <div className="grid gap-2">
            {sampleQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => onQuestionClick(question)}
                disabled={isLoading}
                className="text-left p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="text-gray-700 hover:text-primary-700">
                  "{question}"
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
