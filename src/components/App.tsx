import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { UserQuery } from './UserQuery';
import { AIResponse } from './AIResponse';
import { ChatBox } from './ChatBox';
import { useState, useEffect } from "react";
import '../css/sidebar.css'
import '../css/app.css'

function App() {
  const [isOpen, setIsOpen] = useState(false)
  const [isDarkTheme, setIsDarkTheme] = useState(true)

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme)
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
            <UserQuery />
            <AIResponse />
            <UserQuery />
            <AIResponse />
            <AIResponse />
          </div>
          <ChatBox />
        </div>
      </div>
    </main>
  )
}

export default App
