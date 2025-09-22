'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { documentService } from '@/lib/api';
import { DocumentUploadResult } from '@/types';


const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ACCEPTED_FILE_TYPES = {
  'application/pdf': ['.pdf'],
  'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'],
};

interface DocumentUploadProps {
  onUploadSuccess: (document: DocumentUploadResult) => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploading(true);
    setError(null);

    try {
      const result = await documentService.uploadDocument(file);
      onUploadSuccess(result);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Error uploading document';
      setError(errorMessage);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE,
    multiple: false,
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} disabled={uploading} />
        
        <div className="space-y-4">
          <div className="text-6xl">📄</div>
          
          {uploading ? (
            <div className="space-y-2">
              <div className="text-lg font-medium text-gray-700">
                Processing document...
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full animate-pulse w-1/2"></div>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="text-lg font-medium text-gray-700">
                {isDragActive 
                  ? 'Drop file here...' 
                  : 'Drag a document or click to select'
                }
              </div>
              <div className="text-sm text-gray-500">
                Supports PDF, PNG, JPG, JPEG, TIFF, BMP, GIF (max. 10MB)
              </div>
            </div>
          )}
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-red-800 font-medium">Error</div>
          <div className="text-red-600 text-sm">{error}</div>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;


