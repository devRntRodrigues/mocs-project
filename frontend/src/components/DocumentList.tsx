'use client';

import React, { useEffect, useState } from 'react';
import { documentService } from '@/lib/api';
import { DocumentSummary, DocumentDetail } from '@/types';

interface DocumentListProps {
  onSelectDocument: (document: DocumentDetail) => void;
  selectedDocumentId?: number;
}

const DocumentList: React.FC<DocumentListProps> = ({ 
  onSelectDocument, 
  selectedDocumentId 
}) => {
  const [documents, setDocuments] = useState<DocumentSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const docs = await documentService.listDocuments();
      setDocuments(docs);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Error loading documents';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentClick = async (docSummary: DocumentSummary) => {
    try {
      const fullDocument = await documentService.getDocument(docSummary.id);
      onSelectDocument(fullDocument);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Error loading full document';
      setError(errorMessage);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US');
  };

  const formatFileSize = (length: number): string => {
    if (length < 1000) return `${length} chars`;
    if (length < 1000000) return `${(length / 1000).toFixed(1)}k chars`;
    return `${(length / 1000000).toFixed(1)}M chars`;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Processed Documents
        </h2>
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Processed Documents
        </h2>
        <div className="text-red-600">{error}</div>
        <button
          onClick={loadDocuments}
          className="mt-2 text-blue-600 hover:text-blue-800"
        >
          Try again
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Processed Documents
        </h2>
        <button
          onClick={loadDocuments}
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          Refresh
        </button>
      </div>

      {documents.length === 0 ? (
        <div className="text-gray-500 text-center py-8">
          No documents processed yet.
          <br />
          Upload a document to get started.
        </div>
      ) : (
        <div className="space-y-3">
          {documents.map((doc) => (
            <div
              key={doc.id}
              onClick={() => handleDocumentClick(doc)}
              className={`
                p-4 border rounded-lg cursor-pointer transition-colors
                ${selectedDocumentId === doc.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }
              `}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900 mb-1">
                    {doc.file_name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">
                    Size: {formatFileSize(doc.text_length)}
                  </p>
                  <div className="text-xs text-gray-500">
                    Processed on: {formatDate(doc.created_at)}
                  </div>
                </div>
                <div className="ml-4 text-xs text-gray-400">
                  ID: {doc.id}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocumentList;


