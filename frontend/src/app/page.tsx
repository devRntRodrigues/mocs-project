'use client';

import React, { useState } from 'react';
import DocumentUpload from '@/components/DocumentUpload';
import DocumentViewer from '@/components/DocumentViewer';
import QuestionAnswer from '@/components/QuestionAnswer';
import DocumentList from '@/components/DocumentList';
import { DocumentDetail, DocumentUploadResult } from '@/types';

export default function Home() {
  const [selectedDocument, setSelectedDocument] = useState<DocumentDetail | null>(null);
  const [uploadedDocument, setUploadedDocument] = useState<DocumentUploadResult | null>(null);

  const handleUploadSuccess = (document: DocumentUploadResult) => {
    setUploadedDocument(document);
    // Convert uploaded document to DocumentDetail type for selection
    const doc: DocumentDetail = {
      id: document.id,
      file_name: document.file_name,
      text_content: document.text_content,
      created_at: document.created_at,
    };
    setSelectedDocument(doc);
  };

  const handleSelectDocument = (document: DocumentDetail) => {
    setSelectedDocument(document);
    setUploadedDocument(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">
              📄 Document Processor
            </h1>
            <p className="mt-2 text-gray-600">
              Document digitization and analysis with OCR and AI
            </p>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!selectedDocument ? (
          /* Upload and List View */
          <div className="space-y-8">
            {/* Upload Section */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
                Upload a document
              </h2>
              <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            </section>

            {/* Document List */}
            <section>
              <DocumentList 
                onSelectDocument={handleSelectDocument}
              />
            </section>
          </div>
        ) : (
          /* Document View */
          <div className="space-y-8">
            {/* Back Button */}
            <div>
              <button
                onClick={() => {
                  setSelectedDocument(null);
                  setUploadedDocument(null);
                }}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                ← Back to list
              </button>
            </div>

            {/* Success Message for Upload */}
            {uploadedDocument && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">
                      Document processed successfully!
                    </h3>
                    <div className="mt-2 text-sm text-green-700">
                      <p>Document processed with {uploadedDocument.rag_processing.chunks_created} chunks in {uploadedDocument.processing_time_ms}ms</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Document Viewer */}
              <div>
                <DocumentViewer document={selectedDocument} />
              </div>

              {/* Question & Answer */}
              <div>
                <QuestionAnswer 
                  documentId={selectedDocument.id}
                  documentName={selectedDocument.file_name}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>Document Processor - Developed for MOCS</p>
            <p className="mt-1">
              Technologies: Python • FastAPI • Next.js • TypeScript • PostgreSQL • OCR • RAG
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}