export interface Flashcard {
  id: string;
  question: string;
  answer: string;
}

export interface FlashcardSet {
  id: string;
  title: string;
  description?: string;
  cards: Flashcard[];
  createdAt: Date;
}

export interface UploadState {
  isUploading: boolean;
  isGenerating: boolean;
  progress: number;
  error?: string;
}
