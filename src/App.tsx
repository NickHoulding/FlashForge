import { useState } from "react";
import { FileUpload } from "@/components/FileUpload";
import { FlashcardView } from "@/components/FlashcardView";
import type { Flashcard, UploadState } from "@/types/flashcard";
import "./index.css";

export function App() {
  const [uploadState, setUploadState] = useState<UploadState>({
    isUploading: false,
    isGenerating: false,
    progress: 0,
  });
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);

  const handleFileSelect = async (file: File) => {
    setUploadState({
      isUploading: true,
      isGenerating: false,
      progress: 0,
    });

    try {
      // TODO: Implement file upload and AI generation logic
      // For now, just simulate the upload
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Mock flashcards for development
      const mockCards: Flashcard[] = [
        {
          id: "1",
          question: "What is React?",
          answer:
            "React is a JavaScript library for building user interfaces, particularly single-page applications.",
        },
        {
          id: "2",
          question: "What is Bun?",
          answer:
            "Bun is a fast all-in-one JavaScript runtime and toolkit designed as a drop-in replacement for Node.js.",
        },
      ];

      setFlashcards(mockCards);
      setUploadState({
        isUploading: false,
        isGenerating: false,
        progress: 100,
      });
    } catch (error) {
      setUploadState({
        isUploading: false,
        isGenerating: false,
        progress: 0,
        error: error instanceof Error ? error.message : "An error occurred",
      });
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto p-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">FlashForge</h1>
          <p className="text-xl text-gray-600">
            Generate AI-powered flashcards from your course documents in seconds
          </p>
        </header>

        <main>
          <FileUpload onFileSelect={handleFileSelect} uploadState={uploadState} />
          {uploadState.isGenerating && (
            <div className="mt-8 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Generating flashcards...</p>
            </div>
          )}
          <FlashcardView cards={flashcards} />
        </main>

        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>Powered by AI and built with Bun + React</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
