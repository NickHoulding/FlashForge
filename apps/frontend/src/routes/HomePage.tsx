import { useState, useEffect } from "react";
import type { ChatMessage } from '../types';
import AIResponse from '../components/AIResponse';
import UserQuery from '../components/UserQuery';
import ChatBox from '../components/ChatBox';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Modal from '../components/Modal';

const HomePage = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme);
  };

  const addMessage = (message: ChatMessage) => {
    setMessages(prev => [...prev, message]);
  };

  useEffect(() => {
    document.documentElement.className = isDarkTheme ? 'dark-theme' : 'light-theme'
  }, [isDarkTheme]);

  return (
    <main className="flex flex-row h-screen">
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      <Sidebar
        isOpen={isOpen}
        onToggleSidebar={toggleSidebar}
      />
      <div className='relative flex flex-row flex-1 h-screen'>
        <Header onToggleTheme={toggleTheme} />
        <div className='flex flex-col w-full max-w-[500px] p-[20px] pt-0 pb-[10px] min-h-0'>
          <div className='flex flex-col gap-[50px] flex-1 py-[75px] w-full mx-auto box-border overflow-auto'>
            {messages.map(message => (
              message.type === 'user' ? (
                <UserQuery 
                  key={message.id} 
                  content={message.content}
                />
              ) : null
            ))}
          </div>
          <ChatBox onSendMessage={addMessage} />
        </div>
        <div className="w-[1px] bg-[var(--secondary)] mt-[75px] mb-[20px] mr-[20px]"></div>
        <div className="w-[10px] flex-1 py-[75px] pr-[20px] flex flex-col gap-[10px] overflow-auto">
          {messages.map(message => (
            message.type === 'ai' ? (
              <AIResponse 
                key={message.id} 
                flashcards={message.flashcards || []}
              />
            ) : null
          ))}
        </div>
      </div>
    </main>
  );
};

export default HomePage;
