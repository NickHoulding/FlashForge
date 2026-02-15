import { useState } from "react";
import type { UploadState } from "@/types/flashcard";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  uploadState: UploadState;
}

export function FileUpload({ onFileSelect, uploadState }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
        dragActive
          ? "border-blue-500 bg-blue-50"
          : "border-gray-300 hover:border-gray-400"
      } ${uploadState.isUploading ? "opacity-50 pointer-events-none" : ""}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-upload"
        className="hidden"
        onChange={handleChange}
        accept=".pdf,.doc,.docx,.txt"
        disabled={uploadState.isUploading}
      />
      <label htmlFor="file-upload" className="cursor-pointer">
        <div className="text-gray-600">
          <svg
            className="mx-auto h-12 w-12 mb-4"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <p className="text-sm font-medium">
            {uploadState.isUploading
              ? "Uploading..."
              : "Drop your course documents here or click to upload"}
          </p>
          <p className="text-xs text-gray-500 mt-2">PDF, DOC, DOCX, or TXT files</p>
        </div>
      </label>
      {uploadState.error && (
        <p className="text-red-500 text-sm mt-4">{uploadState.error}</p>
      )}
    </div>
  );
}
