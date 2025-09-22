'use client';

import React from 'react';
import { DocumentDetail } from '@/types';

interface DocumentViewerProps {
  document: DocumentDetail;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ document }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US');
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="border-b border-gray-200 pb-4 mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Processed Document
        </h2>
        <div className="mt-2 space-y-1 text-sm text-gray-500">
          <div><strong>Name:</strong> {document.file_name}</div>
          <div><strong>Processed on:</strong> {formatDate(document.created_at)}</div>
          <div><strong>ID:</strong> {document.id}</div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-3">
          Extracted Text (OCR)
        </h3>
        <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
          {document.text_content ? (
            <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
              {document.text_content}
            </pre>
          ) : (
            <div className="text-gray-500 italic">
              No text was extracted from the document.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;


