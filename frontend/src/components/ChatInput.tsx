/**
 * Chat input component for submitting queries
 */
import React, { useRef } from "react";
import { useForm } from "react-hook-form";
import { Send, Loader2 } from "lucide-react";
import { cn } from "@/utils/cn";

interface ChatInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

interface FormData {
  query: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  isLoading,
  disabled = false,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors },
  } = useForm<FormData>();

  const query = watch("query");

  const handleFormSubmit = (data: FormData) => {
    if (data.query.trim() && !isLoading) {
      onSubmit(data.query.trim());
      reset();
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(handleFormSubmit)();
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
  };

  const isSubmitDisabled = !query?.trim() || isLoading || disabled;

  return (
    <div className="border-t bg-white p-4">
      <form
        onSubmit={handleSubmit(handleFormSubmit)}
        className="max-w-4xl mx-auto"
      >
        <div className="relative flex items-end gap-2">
          <div className="flex-1">
            <textarea
              {...register("query", {
                required: "Please enter a medical question",
                minLength: {
                  value: 3,
                  message: "Question must be at least 3 characters long",
                },
                maxLength: {
                  value: 1000,
                  message: "Question must be less than 1000 characters",
                },
              })}
              ref={textareaRef}
              placeholder="Ask a medical question... (Press Enter to send, Shift+Enter for new line)"
              className={cn(
                "w-full resize-none rounded-lg border border-gray-300 px-4 py-3 pr-12",
                "focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20",
                "disabled:bg-gray-50 disabled:text-gray-500",
                "min-h-[48px] max-h-[120px]",
                errors.query &&
                  "border-red-500 focus:border-red-500 focus:ring-red-500/20"
              )}
              onKeyDown={handleKeyDown}
              onChange={handleTextareaChange}
              disabled={disabled}
              rows={1}
            />

            {errors.query && (
              <p className="mt-1 text-sm text-red-600">
                {errors.query.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitDisabled}
            className={cn(
              "flex items-center justify-center w-12 h-12 rounded-lg transition-colors",
              "focus:outline-none focus:ring-2 focus:ring-primary-500/20",
              isSubmitDisabled
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700"
            )}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>

        <div className="mt-2 text-xs text-gray-500">
          Ask questions about medical conditions, symptoms, treatments, or
          general health information.
        </div>
      </form>
    </div>
  );
};
