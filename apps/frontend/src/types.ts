import type { ReactNode } from "react";

export interface FlashcardData {
  question: string;
  answer: string;
};

export interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  flashcards?: FlashcardData[];
};

export interface FlashcardProps {
  index: number;
  question?: string;
  answer?: string;
};

export interface AIResponseProps {
  flashcards: FlashcardData[];
};

export interface ChatBoxProps {
  onSendMessage: (message: ChatMessage) => void;
};

export interface UserQueryProps {
  content: string;
};

export interface HeaderProps {
  onToggleTheme: () => void;
};

export interface NavProps {
  onToggleTheme: () => void;
};

export interface SidebarProps {
  isOpen: boolean;
  onToggleSidebar: () => void;
};

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
};

export interface AuthContextType {
  isAuthenticated: boolean;
  setIsAuthenticated: (value: boolean) => void;
};

export interface AuthProviderProps {
  children: ReactNode;
};
