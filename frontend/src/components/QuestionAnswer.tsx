'use client';

import React, { useState } from 'react';
import { ragService } from '@/lib/api';
import { RAGQuestionResponse } from '@/types';

interface QuestionAnswerProps {
  documentId: number;
  documentName: string;
}

const QuestionAnswer: React.FC<QuestionAnswerProps> = ({ documentId, documentName }) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<RAGQuestionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const result = await ragService.askDocumentQuestion(
        documentId,
        question.trim(),
        3
      );
      setAnswer(result);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Error processing question';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    'What is the main subject of the document?',
    'What are the most important pieces of information?',
    'Are there any dates mentioned in the document?',
    'What names are cited in the text?',
    'Are there any monetary values in the document?',
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="border-b border-gray-200 pb-4 mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          Questions & Answers
        </h2>
        <div className="text-sm text-gray-500 mt-1">
          About: <span className="font-medium">{documentName}</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
            Ask a question about the document:
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question here..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
            rows={3}
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Processing...' : 'Send Question'}
        </button>
      </form>

      {/* Suggested Questions */}
      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">
          Suggested questions:
        </h3>
        <div className="space-y-2">
          {suggestedQuestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => setQuestion(suggestion)}
              className="text-left w-full text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 p-2 rounded-md transition-colors"
              disabled={loading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-red-800 font-medium">Error</div>
          <div className="text-red-600 text-sm">{error}</div>
        </div>
      )}

      {/* Answer Display */}
      {answer && (
        <div className="mt-6 space-y-4">
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">
              Answer:
            </h3>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-gray-800 whitespace-pre-wrap">
                {answer.answer}
              </p>
            </div>
          </div>

          {answer.source_chunks.length > 0 && (
            <div>
              <h4 className="text-md font-medium text-gray-700 mb-2">
                Relevant chunks found:
              </h4>
              <div className="space-y-2">
                {answer.source_chunks.map((chunk, index) => (
                  <div key={index} className="bg-gray-50 border border-gray-200 rounded-md p-3">
                    <p className="text-sm text-gray-700">
                      {chunk.content}
                    </p>
                    <div className="mt-2 text-xs text-gray-500">
                      Chunk ID: {chunk.chunk_id} | Document ID: {chunk.document_id}
                      {chunk.source && ` | Source: ${chunk.source}`}
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 text-xs text-gray-500">
                Processed in {answer.processing_time_ms}ms using {answer.method}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestionAnswer;


