import { useState, useEffect } from "react"
import type { ChatMessage } from '../types'
import { AIResponse } from './AIResponse'
import { UserQuery } from './UserQuery'
import { ChatBox } from './ChatBox'
import { Sidebar } from './Sidebar'
import { Header } from './Header'
import '../css/sidebar.css'
import '../css/app.css'
import { Flashcard } from "./Flashcard"

function App() {
  const [isOpen, setIsOpen] = useState(false)
  const [isDarkTheme, setIsDarkTheme] = useState(true)
  const [messages, setMessages] = useState<ChatMessage[]>([])

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme)
  }

  const addMessage = (message: ChatMessage) => {
    setMessages(prev => [...prev, message])
  }

  useEffect(() => {
    document.documentElement.className = isDarkTheme ? 'dark-theme' : 'light-theme'
  }, [isDarkTheme])

  return (
    <main>
      <Sidebar isOpen={isOpen} onToggleSidebar={toggleSidebar} />
      <div className='content'>
        <Header onToggleTheme={toggleTheme}/>
        <div className='chat-root'>
          <div className='chat'>
            {messages.map(message => (
              message.type === 'user' ? (
                <UserQuery key={message.id} content={message.content} />
              ) : null
            ))}
          </div>
          <ChatBox onSendMessage={addMessage}/>
        </div>
        <div className="flash-deck">
          {messages.map(message => (
            message.type === 'ai' ? (
              <AIResponse key={message.id} flashcards={message.flashcards || []} />
            ) : null
          ))}
        </div>
      </div>
    </main>
  )
}

export default App
